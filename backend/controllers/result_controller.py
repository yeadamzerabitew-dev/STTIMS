from flask import request, jsonify
from flask_login import login_required, current_user
from models import TraineeResult, Assessment, Trainee, Enrollment, GradeScale
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime

class ResultController:
    """Controller for results management"""
    
    @staticmethod
    def calculate_percentage(marks_obtained, max_marks):
        """Calculate percentage"""
        if marks_obtained is None or max_marks <= 0:
            return 0
        return round((marks_obtained / max_marks) * 100, 2)
    
    @staticmethod
    def determine_grade(percentage):
        """Determine grade based on Grade_Scale table"""
        if percentage is None:
            return None
        
        # Get grade from Grade_Scale
        grade_scale = GradeScale.query.filter(
            GradeScale.min_percentage <= percentage,
            GradeScale.max_percentage >= percentage
        ).first()
        
        if grade_scale:
            return grade_scale.grade_letter
        return None
    
    @staticmethod
    def determine_pass_fail(percentage, passing_marks, max_marks):
        """Determine if trainee passed"""
        if percentage is None:
            return 'Not Attempted'
        
        # Calculate passing percentage
        if passing_marks is None:
            passing_marks = max_marks * 0.5  # Default 50%
        
        passing_percentage = (passing_marks / max_marks) * 100
        
        if percentage >= passing_percentage:
            return 'Pass'
        return 'Fail'
    
    # =============================================
    # CREATE RESULT
    # =============================================
    
    @staticmethod
    @login_required
    def list_results():
        """List all trainee results with filters and pagination"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            assessment_id = request.args.get('assessment_id', type=int)
            trainee_id = request.args.get('trainee_id', type=int)
            status = request.args.get('status', '')

            query = TraineeResult.query

            if assessment_id:
                query = query.filter(TraineeResult.assessment_id == assessment_id)
            if trainee_id:
                query = query.filter(TraineeResult.trainee_id == trainee_id)
            if status:
                query = query.filter(TraineeResult.status == status)

            query = query.order_by(TraineeResult.recorded_at.desc())
            results = query.paginate(page=page, per_page=per_page, error_out=False)

            return jsonify({
                'results': [result.to_dict() for result in results.items],
                'total': results.total,
                'page': results.page,
                'per_page': results.per_page,
                'pages': results.pages,
                'has_prev': results.has_prev,
                'has_next': results.has_next
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def create_result():
        """Create a new result"""
        try:
            data = request.get_json()
            
            required_fields = ['assessment_id', 'trainee_id', 'marks_obtained']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate assessment
            assessment = Assessment.query.get(data['assessment_id'])
            if not assessment:
                return jsonify({'error': 'Assessment not found'}), 400
            if assessment.status == 'Cancelled':
                return jsonify({'error': 'Cannot add results to cancelled assessment'}), 400
            
            # Validate trainee
            trainee = Trainee.query.get(data['trainee_id'])
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 400
            
            # Check if trainee is enrolled in the batch
            enrollment = Enrollment.query.filter_by(
                trainee_id=data['trainee_id'],
                batch_id=assessment.batch_id
            ).first()
            if not enrollment:
                return jsonify({'error': 'Trainee is not enrolled in this batch'}), 400
            
            # Validate marks
            marks_obtained = data['marks_obtained']
            if marks_obtained < 0 or marks_obtained > assessment.max_marks:
                return jsonify({'error': f'Marks must be between 0 and {assessment.max_marks}'}), 400
            
            # Check for existing result
            existing = TraineeResult.query.filter_by(
                assessment_id=data['assessment_id'],
                trainee_id=data['trainee_id']
            ).first()
            
            # Calculate percentage and grade
            percentage = ResultController.calculate_percentage(
                marks_obtained,
                assessment.max_marks
            )
            grade = ResultController.determine_grade(percentage)
            status = ResultController.determine_pass_fail(
                percentage,
                assessment.passing_marks,
                assessment.max_marks
            )
            
            if existing:
                # Update existing result
                existing.marks_obtained = marks_obtained
                existing.percentage_score = percentage
                existing.grade = grade
                existing.status = status
                existing.comments = data.get('comments', '').strip() if data.get('comments') else None
                existing.instructor_feedback = data.get('instructor_feedback', '').strip() if data.get('instructor_feedback') else None
                existing.recorded_by = current_user.user_id
                existing.recorded_at = datetime.utcnow()
                existing.is_verified = data.get('is_verified', False)
                message = 'Result updated successfully'
            else:
                # Create new result
                result = TraineeResult(
                    assessment_id=data['assessment_id'],
                    trainee_id=data['trainee_id'],
                    marks_obtained=marks_obtained,
                    percentage_score=percentage,
                    grade=grade,
                    status=status,
                    comments=data.get('comments', '').strip() if data.get('comments') else None,
                    instructor_feedback=data.get('instructor_feedback', '').strip() if data.get('instructor_feedback') else None,
                    recorded_by=current_user.user_id,
                    is_verified=data.get('is_verified', False)
                )
                db.session.add(result)
                message = 'Result created successfully'
            
            db.session.commit()
            
            # Update enrollment completion percentage
            ResultController._update_completion_percentage(
                data['trainee_id'],
                assessment.batch_id
            )
            
            return jsonify({
                'message': message,
                'result': {
                    'assessment_id': assessment.assessment_id,
                    'assessment_title': assessment.title,
                    'trainee_id': trainee.trainee_id,
                    'trainee_name': trainee.full_name,
                    'marks_obtained': marks_obtained,
                    'max_marks': assessment.max_marks,
                    'percentage_score': percentage,
                    'grade': grade,
                    'status': status
                }
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def _update_completion_percentage(trainee_id, batch_id):
        """Update completion percentage for an enrollment"""
        # Get all assessments for this batch
        assessments = Assessment.query.filter_by(
            batch_id=batch_id,
            status='Completed'
        ).all()
        
        if not assessments:
            return
        
        # Get results for this trainee
        assessment_ids = [a.assessment_id for a in assessments]
        results = TraineeResult.query.filter(
            TraineeResult.trainee_id == trainee_id,
            TraineeResult.assessment_id.in_(assessment_ids)
        ).all()
        
        if not results:
            return
        
        # Calculate completion percentage
        total_assessments = len(assessments)
        completed = sum(1 for r in results if r.status in ['Pass', 'Fail'])
        percentage = round((completed / total_assessments) * 100, 2)
        
        # Update enrollment
        enrollment = Enrollment.query.filter_by(
            trainee_id=trainee_id,
            batch_id=batch_id
        ).first()
        if enrollment:
            enrollment.completion_percentage = percentage
            db.session.commit()
    
    # =============================================
    # BULK RESULTS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def bulk_results():
        """Create/update results for multiple trainees"""
        try:
            data = request.get_json()
            
            if not data.get('assessment_id'):
                return jsonify({'error': 'Assessment ID is required'}), 400
            if not data.get('results') or not isinstance(data['results'], list):
                return jsonify({'error': 'Results list is required'}), 400
            
            assessment = Assessment.query.get(data['assessment_id'])
            if not assessment:
                return jsonify({'error': 'Assessment not found'}), 400
            if assessment.status == 'Cancelled':
                return jsonify({'error': 'Cannot add results to cancelled assessment'}), 400
            
            results = []
            errors = []
            processed = 0
            
            for item in data['results']:
                try:
                    if not item.get('trainee_id'):
                        errors.append({'error': 'Trainee ID is required', 'item': item})
                        continue
                    
                    trainee = Trainee.query.get(item['trainee_id'])
                    if not trainee:
                        errors.append({'trainee_id': item['trainee_id'], 'error': 'Trainee not found'})
                        continue
                    
                    # Check enrollment
                    enrollment = Enrollment.query.filter_by(
                        trainee_id=item['trainee_id'],
                        batch_id=assessment.batch_id
                    ).first()
                    if not enrollment:
                        errors.append({'trainee_id': item['trainee_id'], 'error': 'Not enrolled in this batch'})
                        continue
                    
                    # Validate marks
                    marks_obtained = item.get('marks_obtained')
                    if marks_obtained is None:
                        errors.append({'trainee_id': item['trainee_id'], 'error': 'Marks are required'})
                        continue
                    
                    if marks_obtained < 0 or marks_obtained > assessment.max_marks:
                        errors.append({
                            'trainee_id': item['trainee_id'],
                            'error': f'Marks must be between 0 and {assessment.max_marks}'
                        })
                        continue
                    
                    # Calculate percentage and grade
                    percentage = ResultController.calculate_percentage(
                        marks_obtained,
                        assessment.max_marks
                    )
                    grade = ResultController.determine_grade(percentage)
                    status = ResultController.determine_pass_fail(
                        percentage,
                        assessment.passing_marks,
                        assessment.max_marks
                    )
                    
                    # Check for existing result
                    existing = TraineeResult.query.filter_by(
                        assessment_id=assessment.assessment_id,
                        trainee_id=item['trainee_id']
                    ).first()
                    
                    if existing:
                        existing.marks_obtained = marks_obtained
                        existing.percentage_score = percentage
                        existing.grade = grade
                        existing.status = status
                        existing.comments = item.get('comments', '').strip() if item.get('comments') else None
                        existing.instructor_feedback = item.get('instructor_feedback', '').strip() if item.get('instructor_feedback') else None
                        existing.recorded_by = current_user.user_id
                        existing.recorded_at = datetime.utcnow()
                    else:
                        result = TraineeResult(
                            assessment_id=assessment.assessment_id,
                            trainee_id=item['trainee_id'],
                            marks_obtained=marks_obtained,
                            percentage_score=percentage,
                            grade=grade,
                            status=status,
                            comments=item.get('comments', '').strip() if item.get('comments') else None,
                            instructor_feedback=item.get('instructor_feedback', '').strip() if item.get('instructor_feedback') else None,
                            recorded_by=current_user.user_id
                        )
                        db.session.add(result)
                    
                    results.append({
                        'trainee_id': item['trainee_id'],
                        'trainee_name': trainee.full_name,
                        'marks_obtained': marks_obtained,
                        'percentage': percentage,
                        'grade': grade,
                        'status': status,
                        'success': True
                    })
                    processed += 1
                    
                except Exception as e:
                    errors.append({
                        'trainee_id': item.get('trainee_id'),
                        'error': str(e)
                    })
            
            db.session.commit()
            
            # Update completion percentages
            for result in results:
                ResultController._update_completion_percentage(
                    result['trainee_id'],
                    assessment.batch_id
                )
            
            return jsonify({
                'message': f'Processed {processed} results',
                'processed': processed,
                'results': results,
                'errors': errors,
                'total_attempted': len(data['results'])
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET ASSESSMENT RESULTS
    # =============================================
    
    @staticmethod
    @login_required
    def get_assessment_results(assessment_id):
        """Get results for a specific assessment"""
        try:
            assessment = Assessment.query.get(assessment_id)
            if not assessment:
                return jsonify({'error': 'Assessment not found'}), 404
            
            # Get all enrolled trainees for this batch
            enrollments = Enrollment.query.filter_by(
                batch_id=assessment.batch_id,
                status='Active'
            ).all()
            
            results_list = []
            passed_count = 0
            failed_count = 0
            not_attempted = 0
            total_marks = 0
            
            for enrollment in enrollments:
                result = TraineeResult.query.filter_by(
                    assessment_id=assessment_id,
                    trainee_id=enrollment.trainee_id
                ).first()
                
                if result:
                    if result.status == 'Pass':
                        passed_count += 1
                    elif result.status == 'Fail':
                        failed_count += 1
                    else:
                        not_attempted += 1
                    
                    if result.marks_obtained is not None:
                        total_marks += result.marks_obtained
                    
                    results_list.append({
                        'trainee_id': enrollment.trainee_id,
                        'trainee_code': enrollment.trainee.trainee_code,
                        'trainee_name': enrollment.trainee.full_name,
                        'marks_obtained': float(result.marks_obtained) if result.marks_obtained is not None else None,
                        'percentage_score': float(result.percentage_score) if result.percentage_score is not None else None,
                        'grade': result.grade,
                        'status': result.status,
                        'comments': result.comments,
                        'instructor_feedback': result.instructor_feedback,
                        'recorded_at': result.recorded_at.isoformat() if result.recorded_at else None,
                        'is_verified': result.is_verified
                    })
                else:
                    not_attempted += 1
                    results_list.append({
                        'trainee_id': enrollment.trainee_id,
                        'trainee_code': enrollment.trainee.trainee_code,
                        'trainee_name': enrollment.trainee.full_name,
                        'marks_obtained': None,
                        'percentage_score': None,
                        'grade': None,
                        'status': 'Not Attempted',
                        'comments': None,
                        'instructor_feedback': None,
                        'recorded_at': None,
                        'is_verified': False
                    })
            
            total_enrolled = len(results_list)
            average_marks = round(total_marks / len(results_list), 2) if results_list else 0
            
            return jsonify({
                'assessment': assessment.to_dict_minimal(),
                'summary': {
                    'total_enrolled': total_enrolled,
                    'passed': passed_count,
                    'failed': failed_count,
                    'not_attempted': not_attempted,
                    'pass_rate': round((passed_count / total_enrolled) * 100, 2) if total_enrolled > 0 else 0,
                    'average_marks': average_marks
                },
                'data': results_list
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET TRAINEE RESULTS
    # =============================================
    
    @staticmethod
    @login_required
    def get_trainee_results(trainee_id):
        """Get results for a specific trainee"""
        try:
            trainee = Trainee.query.get(trainee_id)
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 404
            
            # Get all enrollments for this trainee
            enrollments = Enrollment.query.filter_by(
                trainee_id=trainee_id,
                status='Active'
            ).all()
            
            results_by_batch = []
            
            for enrollment in enrollments:
                # Get all assessments for this batch
                assessments = Assessment.query.filter_by(
                    batch_id=enrollment.batch_id
                ).order_by(Assessment.assessment_date).all()
                
                assessment_results = []
                total_marks = 0
                total_max_marks = 0
                passed_count = 0
                
                for assessment in assessments:
                    result = TraineeResult.query.filter_by(
                        assessment_id=assessment.assessment_id,
                        trainee_id=trainee_id
                    ).first()
                    
                    if result:
                        if result.status == 'Pass':
                            passed_count += 1
                        if result.marks_obtained is not None:
                            total_marks += result.marks_obtained
                            total_max_marks += assessment.max_marks
                        
                        assessment_results.append({
                            'assessment_id': assessment.assessment_id,
                            'title': assessment.title,
                            'type': assessment.assessment_type,
                            'max_marks': assessment.max_marks,
                            'weightage': assessment.weightage_percent,
                            'marks_obtained': float(result.marks_obtained) if result.marks_obtained is not None else None,
                            'percentage_score': float(result.percentage_score) if result.percentage_score is not None else None,
                            'grade': result.grade,
                            'status': result.status
                        })
                    else:
                        assessment_results.append({
                            'assessment_id': assessment.assessment_id,
                            'title': assessment.title,
                            'type': assessment.assessment_type,
                            'max_marks': assessment.max_marks,
                            'weightage': assessment.weightage_percent,
                            'marks_obtained': None,
                            'percentage_score': None,
                            'grade': None,
                            'status': 'Not Attempted'
                        })
                
                overall_percentage = round((total_marks / total_max_marks) * 100, 2) if total_max_marks > 0 else 0
                
                results_by_batch.append({
                    'batch_id': enrollment.batch_id,
                    'batch_name': enrollment.batch.batch_name,
                    'course_title': enrollment.batch.course.course_title,
                    'total_assessments': len(assessments),
                    'passed_count': passed_count,
                    'overall_percentage': overall_percentage,
                    'grade': ResultController.determine_grade(overall_percentage),
                    'attendance_percentage': enrollment.attendance_percentage,
                    'completion_percentage': enrollment.completion_percentage,
                    'assessments': assessment_results
                })
            
            return jsonify({
                'trainee_id': trainee_id,
                'trainee_name': trainee.full_name,
                'results_by_batch': results_by_batch
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # VERIFY RESULT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def verify_result(result_id):
        """Verify a result"""
        try:
            result = TraineeResult.query.get(result_id)
            if not result:
                return jsonify({'error': 'Result not found'}), 404
            
            result.is_verified = True
            db.session.commit()
            
            return jsonify({
                'message': 'Result verified successfully',
                'result': {
                    'id': result.result_id,
                    'trainee_id': result.trainee_id,
                    'assessment_id': result.assessment_id,
                    'status': result.status,
                    'verified': result.is_verified
                }
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET RESULT STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_result_stats():
        """Get result statistics"""
        try:
            total = TraineeResult.query.count()
            passed = TraineeResult.query.filter_by(status='Pass').count()
            failed = TraineeResult.query.filter_by(status='Fail').count()
            not_attempted = TraineeResult.query.filter_by(status='Not Attempted').count()
            
            # Grade distribution
            grade_stats = {}
            grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
            for grade in grades:
                grade_stats[grade] = TraineeResult.query.filter_by(grade=grade).count()
            
            # Verified stats
            verified = TraineeResult.query.filter_by(is_verified=True).count()
            unverified = TraineeResult.query.filter_by(is_verified=False).count()
            
            # Average scores
            avg_marks = db.session.query(db.func.avg(TraineeResult.marks_obtained)).scalar() or 0
            avg_percentage = db.session.query(db.func.avg(TraineeResult.percentage_score)).scalar() or 0
            
            return jsonify({
                'total_results': total,
                'passed': passed,
                'failed': failed,
                'not_attempted': not_attempted,
                'pass_rate': round((passed / (passed + failed)) * 100, 2) if (passed + failed) > 0 else 0,
                'grade_distribution': grade_stats,
                'verification': {
                    'verified': verified,
                    'unverified': unverified,
                    'verification_rate': round((verified / total) * 100, 2) if total > 0 else 0
                },
                'average_marks': round(avg_marks, 2),
                'average_percentage': round(avg_percentage, 2)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

