from flask import request, jsonify
from flask_login import login_required, current_user
from models import Assessment, Batch, User
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime, date
import re

class AssessmentController:
    """Controller for assessment management"""
    
    @staticmethod
    def generate_assessment_code(batch_id, title):
        """Generate a unique assessment code"""
        batch = Batch.query.get(batch_id)
        if not batch:
            return f"A-{batch_id}-{datetime.now().strftime('%Y%m%d')}"
        # Take first 3 letters of each word
        words = title.split()
        code = ''.join([word[:3].upper() for word in words[:2]])
        return f"A-{batch.batch_code}-{code}-{datetime.now().strftime('%m%d')}"
    
    # =============================================
    # CREATE ASSESSMENT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def create_assessment():
        """Create a new assessment"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['batch_id', 'title', 'assessment_type', 'max_marks', 'weightage_percent', 'assessment_date']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate batch
            batch = Batch.query.get(data['batch_id'])
            if not batch:
                return jsonify({'error': 'Batch not found'}), 400
            if batch.status in ['Completed', 'Cancelled']:
                return jsonify({'error': 'Cannot add assessments to completed/cancelled batch'}), 400
            
            # Validate assessment type
            valid_types = ['Quiz', 'Midterm', 'Final', 'Practical', 'Project', 'Assignment', 'Lab', 'Presentation']
            if data['assessment_type'] not in valid_types:
                return jsonify({'error': 'Invalid assessment type'}), 400
            
            # Validate max marks
            if data['max_marks'] <= 0:
                return jsonify({'error': 'Maximum marks must be greater than 0'}), 400
            
            # Validate weightage
            if data['weightage_percent'] <= 0 or data['weightage_percent'] > 100:
                return jsonify({'error': 'Weightage must be between 1 and 100'}), 400
            
            # Check total weightage for batch
            existing_weightage = db.session.query(db.func.sum(Assessment.weightage_percent)).filter(
                Assessment.batch_id == data['batch_id'],
                Assessment.status != 'Cancelled'
            ).scalar() or 0
            
            if existing_weightage + data['weightage_percent'] > 100:
                return jsonify({
                    'error': f'Total weightage would exceed 100%. Current total: {existing_weightage}%'
                }), 400
            
            # Validate passing marks
            passing_marks = data.get('passing_marks')
            if passing_marks is not None:
                if passing_marks < 0 or passing_marks > data['max_marks']:
                    return jsonify({'error': 'Passing marks must be between 0 and max marks'}), 400
            
            # Validate assessment date
            try:
                assessment_date = datetime.strptime(data['assessment_date'], '%Y-%m-%d').date()
                if assessment_date < batch.start_date or assessment_date > batch.end_date:
                    return jsonify({'error': f'Assessment date must be between {batch.start_date} and {batch.end_date}'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
            # Validate times if provided
            start_time = None
            end_time = None
            if data.get('start_time'):
                try:
                    start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
                except ValueError:
                    return jsonify({'error': 'Invalid start time format. Use HH:MM:SS'}), 400
            
            if data.get('end_time'):
                try:
                    end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
                except ValueError:
                    return jsonify({'error': 'Invalid end time format. Use HH:MM:SS'}), 400
            
            if start_time and end_time and start_time >= end_time:
                return jsonify({'error': 'Start time must be before end time'}), 400
            
            # Generate assessment code
            assessment_code = AssessmentController.generate_assessment_code(
                data['batch_id'],
                data['title']
            )
            
            # Create assessment
            assessment = Assessment(
                assessment_code=assessment_code,
                batch_id=data['batch_id'],
                title=data['title'].strip(),
                description=data.get('description', '').strip() if data.get('description') else None,
                assessment_type=data['assessment_type'],
                max_marks=data['max_marks'],
                weightage_percent=data['weightage_percent'],
                passing_marks=passing_marks,
                assessment_date=assessment_date,
                start_time=start_time,
                end_time=end_time,
                duration_minutes=data.get('duration_minutes'),
                total_questions=data.get('total_questions'),
                instructions=data.get('instructions', '').strip() if data.get('instructions') else None,
                status='Scheduled',
                created_by=current_user.user_id
            )
            
            db.session.add(assessment)
            db.session.commit()
            
            return jsonify({
                'message': 'Assessment created successfully',
                'assessment': assessment.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # LIST ASSESSMENTS
    # =============================================
    
    @staticmethod
    @login_required
    def list_assessments():
        """List all assessments with filters"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            batch_id = request.args.get('batch_id', type=int)
            assessment_type = request.args.get('assessment_type', '')
            status = request.args.get('status', '')
            
            query = Assessment.query
            
            if batch_id:
                query = query.filter(Assessment.batch_id == batch_id)
            if assessment_type:
                query = query.filter(Assessment.assessment_type == assessment_type)
            if status:
                query = query.filter(Assessment.status == status)
            
            query = query.order_by(Assessment.assessment_date.asc())
            assessments = query.paginate(page=page, per_page=per_page, error_out=False)
            
            # Get weightage totals
            total_weightage = db.session.query(db.func.sum(Assessment.weightage_percent)).filter(
                Assessment.batch_id == batch_id if batch_id else True,
                Assessment.status != 'Cancelled'
            ).scalar() or 0
            
            return jsonify({
                'data': [assessment.to_dict() for assessment in assessments.items],
                'total': assessments.total,
                'page': assessments.page,
                'per_page': assessments.per_page,
                'total_pages': assessments.pages,
                'total_weightage': round(total_weightage, 2)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET ASSESSMENT DETAILS
    # =============================================
    
    @staticmethod
    @login_required
    def get_assessment(assessment_id):
        """Get assessment details by ID"""
        try:
            assessment = Assessment.query.get(assessment_id)
            if not assessment:
                return jsonify({'error': 'Assessment not found'}), 404
            
            # Get results count
            results_count = assessment.results.count()
            passed_count = assessment.results.filter_by(status='Pass').count()
            failed_count = assessment.results.filter_by(status='Fail').count()
            
            return jsonify({
                'assessment': assessment.to_dict(),
                'statistics': {
                    'results_count': results_count,
                    'passed': passed_count,
                    'failed': failed_count,
                    'pass_rate': round((passed_count / results_count) * 100, 2) if results_count > 0 else 0
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # UPDATE ASSESSMENT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def update_assessment(assessment_id):
        """Update an existing assessment"""
        try:
            assessment = Assessment.query.get(assessment_id)
            if not assessment:
                return jsonify({'error': 'Assessment not found'}), 404
            
            if assessment.status == 'Completed':
                return jsonify({'error': 'Cannot update completed assessment'}), 400
            
            data = request.get_json()
            
            # Update title
            if data.get('title'):
                assessment.title = data['title'].strip()
            
            # Update description
            if data.get('description') is not None:
                assessment.description = data['description'].strip() if data['description'] else None
            
            # Update assessment type
            if data.get('assessment_type'):
                valid_types = ['Quiz', 'Midterm', 'Final', 'Practical', 'Project', 'Assignment', 'Lab', 'Presentation']
                if data['assessment_type'] not in valid_types:
                    return jsonify({'error': 'Invalid assessment type'}), 400
                assessment.assessment_type = data['assessment_type']
            
            # Update max marks
            if data.get('max_marks'):
                if data['max_marks'] <= 0:
                    return jsonify({'error': 'Maximum marks must be greater than 0'}), 400
                assessment.max_marks = data['max_marks']
            
            # Update weightage
            if data.get('weightage_percent'):
                if data['weightage_percent'] <= 0 or data['weightage_percent'] > 100:
                    return jsonify({'error': 'Weightage must be between 1 and 100'}), 400
                
                # Check total weightage
                existing_total = db.session.query(db.func.sum(Assessment.weightage_percent)).filter(
                    Assessment.batch_id == assessment.batch_id,
                    Assessment.assessment_id != assessment_id,
                    Assessment.status != 'Cancelled'
                ).scalar() or 0
                
                if existing_total + data['weightage_percent'] > 100:
                    return jsonify({
                        'error': f'Total weightage would exceed 100%. Current total: {existing_total}%'
                    }), 400
                
                assessment.weightage_percent = data['weightage_percent']
            
            # Update passing marks
            if data.get('passing_marks') is not None:
                if data['passing_marks'] < 0 or data['passing_marks'] > assessment.max_marks:
                    return jsonify({'error': 'Passing marks must be between 0 and max marks'}), 400
                assessment.passing_marks = data['passing_marks']
            
            # Update assessment date
            if data.get('assessment_date'):
                try:
                    assessment_date = datetime.strptime(data['assessment_date'], '%Y-%m-%d').date()
                    batch = Batch.query.get(assessment.batch_id)
                    if assessment_date < batch.start_date or assessment_date > batch.end_date:
                        return jsonify({'error': f'Assessment date must be between {batch.start_date} and {batch.end_date}'}), 400
                    assessment.assessment_date = assessment_date
                except ValueError:
                    return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
            # Update times
            if data.get('start_time') is not None:
                if data['start_time']:
                    try:
                        assessment.start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
                    except ValueError:
                        return jsonify({'error': 'Invalid start time format. Use HH:MM:SS'}), 400
                else:
                    assessment.start_time = None
            
            if data.get('end_time') is not None:
                if data['end_time']:
                    try:
                        assessment.end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
                    except ValueError:
                        return jsonify({'error': 'Invalid end time format. Use HH:MM:SS'}), 400
                else:
                    assessment.end_time = None
            
            # Update duration
            if data.get('duration_minutes') is not None:
                assessment.duration_minutes = data['duration_minutes']
            
            # Update total questions
            if data.get('total_questions') is not None:
                assessment.total_questions = data['total_questions']
            
            # Update instructions
            if data.get('instructions') is not None:
                assessment.instructions = data['instructions'].strip() if data['instructions'] else None
            
            # Update status
            if data.get('status'):
                valid_statuses = ['Scheduled', 'Ongoing', 'Completed', 'Cancelled']
                if data['status'] not in valid_statuses:
                    return jsonify({'error': 'Invalid status'}), 400
                assessment.status = data['status']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Assessment updated successfully',
                'assessment': assessment.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # CANCEL ASSESSMENT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def cancel_assessment(assessment_id):
        """Cancel an assessment"""
        try:
            assessment = Assessment.query.get(assessment_id)
            if not assessment:
                return jsonify({'error': 'Assessment not found'}), 404
            
            if assessment.status == 'Completed':
                return jsonify({'error': 'Cannot cancel completed assessment'}), 400
            
            if assessment.status == 'Cancelled':
                return jsonify({'error': 'Assessment is already cancelled'}), 400
            
            assessment.status = 'Cancelled'
            db.session.commit()
            
            return jsonify({
                'message': f'Assessment "{assessment.title}" cancelled successfully',
                'assessment': assessment.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # COMPLETE ASSESSMENT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def complete_assessment(assessment_id):
        """Mark assessment as completed"""
        try:
            assessment = Assessment.query.get(assessment_id)
            if not assessment:
                return jsonify({'error': 'Assessment not found'}), 404
            
            if assessment.status == 'Completed':
                return jsonify({'error': 'Assessment is already completed'}), 400
            
            if assessment.status == 'Cancelled':
                return jsonify({'error': 'Cannot complete cancelled assessment'}), 400
            
            # Check if all results are recorded
            enrolled_count = Batch.query.get(assessment.batch_id).enrollments.filter_by(
                status='Active'
            ).count()
            
            results_count = assessment.results.count()
            
            if results_count < enrolled_count:
                return jsonify({
                    'error': f'Not all results are recorded. {results_count}/{enrolled_count} recorded'
                }), 400
            
            assessment.status = 'Completed'
            db.session.commit()
            
            return jsonify({
                'message': f'Assessment "{assessment.title}" completed successfully',
                'assessment': assessment.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET ASSESSMENT STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_assessment_stats():
        """Get assessment statistics"""
        try:
            total = Assessment.query.count()
            scheduled = Assessment.query.filter_by(status='Scheduled').count()
            ongoing = Assessment.query.filter_by(status='Ongoing').count()
            completed = Assessment.query.filter_by(status='Completed').count()
            cancelled = Assessment.query.filter_by(status='Cancelled').count()
            
            # Type breakdown
            type_stats = {}
            types = ['Quiz', 'Midterm', 'Final', 'Practical', 'Project', 'Assignment', 'Lab', 'Presentation']
            for atype in types:
                type_stats[atype] = Assessment.query.filter_by(assessment_type=atype).count()
            
            # Average weightage
            avg_weightage = db.session.query(db.func.avg(Assessment.weightage_percent)).scalar() or 0
            
            return jsonify({
                'total_assessments': total,
                'scheduled': scheduled,
                'ongoing': ongoing,
                'completed': completed,
                'cancelled': cancelled,
                'type_breakdown': type_stats,
                'average_weightage': round(avg_weightage, 2)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
