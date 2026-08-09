from flask import request, jsonify
from flask_login import login_required, current_user
from models import AttendanceRecord, ClassSession, Trainee, Enrollment
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime, date

class AttendanceController:
    """Controller for attendance management"""
    
    @staticmethod
    def _update_attendance_percentage(trainee_id, batch_id):
        """Update attendance percentage for an enrollment"""
        # Get all sessions for this batch
        sessions = ClassSession.query.filter_by(
            batch_id=batch_id,
            status='Completed'
        ).all()
        
        if not sessions:
            return
        
        # Get attendance records for this trainee
        session_ids = [s.session_id for s in sessions]
        records = AttendanceRecord.query.filter(
            AttendanceRecord.trainee_id == trainee_id,
            AttendanceRecord.session_id.in_(session_ids)
        ).all()
        
        if not records:
            return
        
        total_sessions = len(sessions)
        present_count = sum(1 for r in records if r.status in ['Present', 'Late'])
        
        percentage = round((present_count / total_sessions) * 100, 2) if total_sessions > 0 else 0
        
        # Update enrollment
        enrollment = Enrollment.query.filter_by(
            trainee_id=trainee_id,
            batch_id=batch_id
        ).first()
        if enrollment:
            enrollment.attendance_percentage = percentage
            db.session.commit()
    
    # =============================================
    # LIST ALL ATTENDANCE RECORDS
    # =============================================
    
    @staticmethod
    @login_required
    def list_attendance():
        """List all attendance records with filters and pagination"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            session_id = request.args.get('session_id', type=int)
            trainee_id = request.args.get('trainee_id', type=int)
            batch_id = request.args.get('batch_id', type=int)
            status = request.args.get('status', '')
            date_from = request.args.get('date_from')
            date_to = request.args.get('date_to')

            query = AttendanceRecord.query

            if session_id:
                query = query.filter(AttendanceRecord.session_id == session_id)
            if trainee_id:
                query = query.filter(AttendanceRecord.trainee_id == trainee_id)
            if batch_id:
                query = query.join(ClassSession).filter(ClassSession.batch_id == batch_id)
            if status:
                query = query.filter(AttendanceRecord.status == status)
            if date_from:
                query = query.join(ClassSession).filter(ClassSession.session_date >= date_from)
            if date_to:
                query = query.join(ClassSession).filter(ClassSession.session_date <= date_to)

            query = query.order_by(AttendanceRecord.recorded_at.desc())
            records = query.paginate(page=page, per_page=per_page, error_out=False)

            return jsonify({
                'attendance': [record.to_dict() for record in records.items],
                'total': records.total,
                'page': records.page,
                'per_page': records.per_page,
                'pages': records.pages,
                'has_prev': records.has_prev,
                'has_next': records.has_next
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # =============================================
    # MARK INDIVIDUAL ATTENDANCE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def mark_attendance():
        """Mark attendance for a single trainee"""
        try:
            data = request.get_json()
            
            required_fields = ['session_id', 'trainee_id', 'status']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate session
            session = ClassSession.query.get(data['session_id'])
            if not session:
                return jsonify({'error': 'Session not found'}), 400
            if session.status == 'Cancelled':
                return jsonify({'error': 'Cannot mark attendance for cancelled session'}), 400
            if session.status == 'Completed':
                return jsonify({'error': 'Cannot mark attendance for completed session'}), 400
            
            # Validate trainee
            trainee = Trainee.query.get(data['trainee_id'])
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 400
            
            # Check if trainee is enrolled in this batch
            enrollment = Enrollment.query.filter_by(
                trainee_id=data['trainee_id'],
                batch_id=session.batch_id
            ).first()
            if not enrollment:
                return jsonify({'error': 'Trainee is not enrolled in this batch'}), 400
            
            # Validate status
            valid_statuses = ['Present', 'Absent', 'Late', 'Excused', 'Holiday', 'Not Applicable']
            if data['status'] not in valid_statuses:
                return jsonify({'error': 'Invalid attendance status'}), 400
            
            # Check for existing record
            existing = AttendanceRecord.query.filter_by(
                session_id=data['session_id'],
                trainee_id=data['trainee_id']
            ).first()
            
            if existing:
                # Update existing record
                existing.status = data['status']
                existing.check_in_time = data.get('check_in_time')
                existing.check_out_time = data.get('check_out_time')
                existing.remarks = data.get('remarks', '').strip() if data.get('remarks') else None
                existing.recorded_by = current_user.user_id
                existing.is_verified = data.get('is_verified', False)
                existing.recorded_at = datetime.utcnow()
                message = 'Attendance updated successfully'
            else:
                # Create new record
                record = AttendanceRecord(
                    session_id=data['session_id'],
                    trainee_id=data['trainee_id'],
                    status=data['status'],
                    check_in_time=data.get('check_in_time'),
                    check_out_time=data.get('check_out_time'),
                    remarks=data.get('remarks', '').strip() if data.get('remarks') else None,
                    recorded_by=current_user.user_id,
                    is_verified=data.get('is_verified', False)
                )
                db.session.add(record)
                message = 'Attendance marked successfully'
            
            db.session.commit()
            
            # Update attendance percentage in enrollment
            AttendanceController._update_attendance_percentage(
                data['trainee_id'],
                session.batch_id
            )
            
            return jsonify({
                'message': message,
                'attendance': {
                    'session_id': data['session_id'],
                    'trainee_id': data['trainee_id'],
                    'trainee_name': trainee.full_name,
                    'status': data['status']
                }
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # BULK ATTENDANCE MARKING
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def bulk_attendance():
        """Mark attendance for multiple trainees in a session"""
        try:
            data = request.get_json()
            
            if not data.get('session_id'):
                return jsonify({'error': 'Session ID is required'}), 400
            if not data.get('attendance') or not isinstance(data['attendance'], list):
                return jsonify({'error': 'Attendance list is required'}), 400
            
            session = ClassSession.query.get(data['session_id'])
            if not session:
                return jsonify({'error': 'Session not found'}), 400
            if session.status == 'Cancelled':
                return jsonify({'error': 'Cannot mark attendance for cancelled session'}), 400
            if session.status == 'Completed':
                return jsonify({'error': 'Cannot mark attendance for completed session'}), 400
            
            results = []
            errors = []
            processed = 0
            
            for item in data['attendance']:
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
                        batch_id=session.batch_id
                    ).first()
                    if not enrollment:
                        errors.append({'trainee_id': item['trainee_id'], 'error': 'Not enrolled in this batch'})
                        continue
                    
                    # Validate status
                    status = item.get('status', 'Absent')
                    valid_statuses = ['Present', 'Absent', 'Late', 'Excused', 'Holiday', 'Not Applicable']
                    if status not in valid_statuses:
                        errors.append({'trainee_id': item['trainee_id'], 'error': f'Invalid status: {status}'})
                        continue
                    
                    # Check for existing record
                    existing = AttendanceRecord.query.filter_by(
                        session_id=session.session_id,
                        trainee_id=item['trainee_id']
                    ).first()
                    
                    if existing:
                        existing.status = status
                        existing.check_in_time = item.get('check_in_time')
                        existing.check_out_time = item.get('check_out_time')
                        existing.remarks = item.get('remarks', '').strip() if item.get('remarks') else None
                        existing.recorded_by = current_user.user_id
                        existing.recorded_at = datetime.utcnow()
                    else:
                        record = AttendanceRecord(
                            session_id=session.session_id,
                            trainee_id=item['trainee_id'],
                            status=status,
                            check_in_time=item.get('check_in_time'),
                            check_out_time=item.get('check_out_time'),
                            remarks=item.get('remarks', '').strip() if item.get('remarks') else None,
                            recorded_by=current_user.user_id
                        )
                        db.session.add(record)
                    
                    results.append({
                        'trainee_id': item['trainee_id'],
                        'trainee_name': trainee.full_name,
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
            
            # Update attendance percentages for all processed trainees
            for result in results:
                AttendanceController._update_attendance_percentage(
                    result['trainee_id'],
                    session.batch_id
                )
            
            return jsonify({
                'message': f'Processed {processed} attendance records',
                'processed': processed,
                'results': results,
                'errors': errors,
                'total_attempted': len(data['attendance'])
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET SESSION ATTENDANCE
    # =============================================
    
    @staticmethod
    @login_required
    def get_session_attendance(session_id):
        """Get attendance for a specific session"""
        try:
            session = ClassSession.query.get(session_id)
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            # Get all enrolled trainees for this batch
            enrollments = Enrollment.query.filter_by(
                batch_id=session.batch_id,
                status='Active'
            ).all()
            
            attendance_list = []
            present_count = 0
            absent_count = 0
            late_count = 0
            excused_count = 0
            
            for enrollment in enrollments:
                record = AttendanceRecord.query.filter_by(
                    session_id=session_id,
                    trainee_id=enrollment.trainee_id
                ).first()
                
                status = record.status if record else 'Not Marked'
                
                if status == 'Present':
                    present_count += 1
                elif status == 'Absent':
                    absent_count += 1
                elif status == 'Late':
                    late_count += 1
                elif status == 'Excused':
                    excused_count += 1
                
                attendance_list.append({
                    'trainee_id': enrollment.trainee_id,
                    'trainee_code': enrollment.trainee.trainee_code,
                    'trainee_name': enrollment.trainee.full_name,
                    'status': status,
                    'check_in_time': record.check_in_time.strftime('%H:%M:%S') if record and record.check_in_time else None,
                    'check_out_time': record.check_out_time.strftime('%H:%M:%S') if record and record.check_out_time else None,
                    'remarks': record.remarks if record else None,
                    'recorded_at': record.recorded_at.isoformat() if record and record.recorded_at else None,
                    'recorded_by': record.recorded_by if record else None
                })
            
            total_enrolled = len(attendance_list)
            
            return jsonify({
                'session': session.to_dict_minimal(),
                'summary': {
                    'total_enrolled': total_enrolled,
                    'present': present_count,
                    'absent': absent_count,
                    'late': late_count,
                    'excused': excused_count,
                    'not_marked': total_enrolled - (present_count + absent_count + late_count + excused_count),
                    'attendance_rate': round((present_count / total_enrolled) * 100, 2) if total_enrolled > 0 else 0
                },
                'data': attendance_list
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET TRAINEE ATTENDANCE
    # =============================================
    
    @staticmethod
    @login_required
    def get_trainee_attendance(trainee_id):
        """Get attendance for a specific trainee across all sessions"""
        try:
            trainee = Trainee.query.get(trainee_id)
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 404
            
            # Get all enrollments for this trainee
            enrollments = Enrollment.query.filter_by(
                trainee_id=trainee_id,
                status='Active'
            ).all()
            
            attendance_by_batch = []
            
            for enrollment in enrollments:
                # Get all sessions for this batch
                sessions = ClassSession.query.filter_by(
                    batch_id=enrollment.batch_id
                ).order_by(ClassSession.session_date).all()
                
                session_attendance = []
                present_count = 0
                total_sessions = len(sessions)
                
                for session in sessions:
                    record = AttendanceRecord.query.filter_by(
                        session_id=session.session_id,
                        trainee_id=trainee_id
                    ).first()
                    
                    status = record.status if record else 'Not Marked'
                    if status in ['Present', 'Late']:
                        present_count += 1
                    
                    session_attendance.append({
                        'session_id': session.session_id,
                        'session_date': session.session_date.isoformat(),
                        'topic': session.topic_covered,
                        'status': status,
                        'check_in_time': record.check_in_time.strftime('%H:%M:%S') if record and record.check_in_time else None,
                        'check_out_time': record.check_out_time.strftime('%H:%M:%S') if record and record.check_out_time else None
                    })
                
                attendance_by_batch.append({
                    'batch_id': enrollment.batch_id,
                    'batch_name': enrollment.batch.batch_name,
                    'course_title': enrollment.batch.course.course_title,
                    'total_sessions': total_sessions,
                    'present_count': present_count,
                    'attendance_percentage': enrollment.attendance_percentage,
                    'sessions': session_attendance
                })
            
            return jsonify({
                'trainee_id': trainee_id,
                'trainee_name': trainee.full_name,
                'attendance_by_batch': attendance_by_batch
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # VERIFY ATTENDANCE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def verify_attendance(record_id):
        """Verify an attendance record"""
        try:
            record = AttendanceRecord.query.get(record_id)
            if not record:
                return jsonify({'error': 'Attendance record not found'}), 404
            
            record.is_verified = True
            db.session.commit()
            
            return jsonify({
                'message': 'Attendance verified successfully',
                'record': {
                    'session_id': record.session_id,
                    'trainee_id': record.trainee_id,
                    'status': record.status,
                    'verified': record.is_verified
                }
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET ATTENDANCE STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_attendance_stats():
        """Get attendance statistics"""
        try:
            total_records = AttendanceRecord.query.count()
            
            # Count by status
            present = AttendanceRecord.query.filter_by(status='Present').count()
            absent = AttendanceRecord.query.filter_by(status='Absent').count()
            late = AttendanceRecord.query.filter_by(status='Late').count()
            excused = AttendanceRecord.query.filter_by(status='Excused').count()
            
            # Verify stats
            verified = AttendanceRecord.query.filter_by(is_verified=True).count()
            unverified = AttendanceRecord.query.filter_by(is_verified=False).count()
            
            # Overall attendance rate
            total_marked = present + absent + late + excused
            attendance_rate = round((present / total_marked) * 100, 2) if total_marked > 0 else 0
            
            return jsonify({
                'total_records': total_records,
                'breakdown': {
                    'present': present,
                    'absent': absent,
                    'late': late,
                    'excused': excused,
                    'not_marked': 0  # Calculated separately
                },
                'verification': {
                    'verified': verified,
                    'unverified': unverified,
                    'verification_rate': round((verified / total_records) * 100, 2) if total_records > 0 else 0
                },
                'attendance_rate': attendance_rate
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
