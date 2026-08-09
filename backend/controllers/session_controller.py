from flask import request, jsonify
from flask_login import login_required, current_user
from models import ClassSession, Batch, Instructor
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime, date
import re

class SessionController:
    """Controller for class session management"""
    
    @staticmethod
    def generate_session_code(batch_id, session_date):
        """Generate a unique session code"""
        batch = Batch.query.get(batch_id)
        if not batch:
            return f"S-{batch_id}-{session_date.strftime('%Y%m%d')}"
        return f"S-{batch.batch_code}-{session_date.strftime('%Y%m%d')}"
    
    # =============================================
    # CREATE SESSION
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def create_session():
        """Create a new class session"""
        try:
            data = request.get_json()
            
            required_fields = ['batch_id', 'session_date', 'start_time', 'end_time', 'instructor_id']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate batch
            batch = Batch.query.get(data['batch_id'])
            if not batch:
                return jsonify({'error': 'Batch not found'}), 400
            if batch.status in ['Completed', 'Cancelled']:
                return jsonify({'error': 'Cannot add sessions to completed/cancelled batch'}), 400
            
            # Validate date
            try:
                session_date = datetime.strptime(data['session_date'], '%Y-%m-%d').date()
                if session_date < date.today():
                    return jsonify({'error': 'Session date cannot be in the past'}), 400
                if session_date < batch.start_date or session_date > batch.end_date:
                    return jsonify({'error': f'Session date must be between {batch.start_date} and {batch.end_date}'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
            # Validate times
            try:
                start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
                end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
                if start_time >= end_time:
                    return jsonify({'error': 'Start time must be before end time'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid time format. Use HH:MM:SS'}), 400
            
            # Validate instructor
            instructor = Instructor.query.get(data['instructor_id'])
            if not instructor:
                return jsonify({'error': 'Instructor not found'}), 400
            if instructor.status != 'Active':
                return jsonify({'error': 'Instructor must be active'}), 400
            
            # Check instructor availability
            existing = ClassSession.query.filter(
                ClassSession.instructor_id == data['instructor_id'],
                ClassSession.session_date == session_date,
                ClassSession.status != 'Cancelled'
            ).filter(
                (ClassSession.start_time < end_time) & (ClassSession.end_time > start_time)
            ).first()
            if existing:
                return jsonify({'error': 'Instructor is already booked at this time'}), 400
            
            # Generate session code
            session_code = SessionController.generate_session_code(data['batch_id'], session_date)
            
            # Create session
            session = ClassSession(
                session_code=session_code,
                batch_id=data['batch_id'],
                session_date=session_date,
                start_time=start_time,
                end_time=end_time,
                topic_covered=data.get('topic_covered', '').strip() if data.get('topic_covered') else None,
                session_type=data.get('session_type', 'Lecture'),
                instructor_id=data['instructor_id'],
                room_number=data.get('room_number', '').strip() if data.get('room_number') else None,
                status='Scheduled',
                notes=data.get('notes', '').strip() if data.get('notes') else None
            )
            
            db.session.add(session)
            db.session.commit()
            
            return jsonify({
                'message': 'Session created successfully',
                'session': session.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # LIST SESSIONS
    # =============================================
    
    @staticmethod
    @login_required
    def list_sessions():
        """List all sessions with filters"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            batch_id = request.args.get('batch_id', type=int)
            instructor_id = request.args.get('instructor_id', type=int)
            status = request.args.get('status', '')
            date_from = request.args.get('date_from')
            date_to = request.args.get('date_to')
            
            query = ClassSession.query
            
            if batch_id:
                query = query.filter(ClassSession.batch_id == batch_id)
            if instructor_id:
                query = query.filter(ClassSession.instructor_id == instructor_id)
            if status:
                query = query.filter(ClassSession.status == status)
            if date_from:
                try:
                    query = query.filter(ClassSession.session_date >= datetime.strptime(date_from, '%Y-%m-%d').date())
                except ValueError:
                    pass
            if date_to:
                try:
                    query = query.filter(ClassSession.session_date <= datetime.strptime(date_to, '%Y-%m-%d').date())
                except ValueError:
                    pass
            
            query = query.order_by(ClassSession.session_date.asc(), ClassSession.start_time.asc())
            sessions = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'data': [session.to_dict() for session in sessions.items],
                'total': sessions.total,
                'page': sessions.page,
                'per_page': sessions.per_page,
                'total_pages': sessions.pages
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET SESSION DETAILS
    # =============================================
    
    @staticmethod
    @login_required
    def get_session(session_id):
        """Get session details by ID"""
        try:
            session = ClassSession.query.get(session_id)
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            # Get attendance count
            attendance_count = session.attendance_records.count()
            present_count = session.attendance_records.filter_by(status='Present').count()
            absent_count = session.attendance_records.filter_by(status='Absent').count()
            late_count = session.attendance_records.filter_by(status='Late').count()
            excused_count = session.attendance_records.filter_by(status='Excused').count()
            
            return jsonify({
                'session': session.to_dict(),
                'attendance_summary': {
                    'total': attendance_count,
                    'present': present_count,
                    'absent': absent_count,
                    'late': late_count,
                    'excused': excused_count,
                    'present_rate': round((present_count / attendance_count) * 100, 2) if attendance_count > 0 else 0
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # UPDATE SESSION
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def update_session(session_id):
        """Update an existing session"""
        try:
            session = ClassSession.query.get(session_id)
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            if session.status == 'Completed':
                return jsonify({'error': 'Cannot update completed session'}), 400
            
            data = request.get_json()
            
            # Update topic covered
            if data.get('topic_covered') is not None:
                session.topic_covered = data['topic_covered'].strip() if data['topic_covered'] else None
            
            # Update session type
            if data.get('session_type'):
                valid_types = ['Lecture', 'Lab', 'Workshop', 'Practical', 'Review', 'Exam']
                if data['session_type'] not in valid_types:
                    return jsonify({'error': 'Invalid session type'}), 400
                session.session_type = data['session_type']
            
            # Update room
            if data.get('room_number') is not None:
                session.room_number = data['room_number'].strip() if data['room_number'] else None
            
            # Update status
            if data.get('status'):
                valid_statuses = ['Scheduled', 'Ongoing', 'Completed', 'Cancelled']
                if data['status'] not in valid_statuses:
                    return jsonify({'error': 'Invalid status'}), 400
                session.status = data['status']
            
            # Update instructor
            if data.get('instructor_id'):
                instructor = Instructor.query.get(data['instructor_id'])
                if not instructor:
                    return jsonify({'error': 'Instructor not found'}), 400
                if instructor.status != 'Active':
                    return jsonify({'error': 'Instructor must be active'}), 400
                
                # Check availability
                existing = ClassSession.query.filter(
                    ClassSession.instructor_id == data['instructor_id'],
                    ClassSession.session_date == session.session_date,
                    ClassSession.session_id != session_id,
                    ClassSession.status != 'Cancelled'
                ).filter(
                    (ClassSession.start_time < session.end_time) & 
                    (ClassSession.end_time > session.start_time)
                ).first()
                if existing:
                    return jsonify({'error': 'Instructor is already booked at this time'}), 400
                session.instructor_id = data['instructor_id']
            
            # Update notes
            if data.get('notes') is not None:
                session.notes = data['notes'].strip() if data['notes'] else None
            
            db.session.commit()
            
            return jsonify({
                'message': 'Session updated successfully',
                'session': session.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # CANCEL SESSION
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def cancel_session(session_id):
        """Cancel a session"""
        try:
            session = ClassSession.query.get(session_id)
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            if session.status == 'Completed':
                return jsonify({'error': 'Cannot cancel completed session'}), 400
            
            if session.status == 'Cancelled':
                return jsonify({'error': 'Session is already cancelled'}), 400
            
            session.status = 'Cancelled'
            db.session.commit()
            
            return jsonify({
                'message': f'Session {session.session_code} cancelled successfully',
                'session': session.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # COMPLETE SESSION
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def complete_session(session_id):
        """Mark session as completed"""
        try:
            session = ClassSession.query.get(session_id)
            if not session:
                return jsonify({'error': 'Session not found'}), 404
            
            if session.status == 'Completed':
                return jsonify({'error': 'Session is already completed'}), 400
            
            if session.status == 'Cancelled':
                return jsonify({'error': 'Cannot complete a cancelled session'}), 400
            
            session.status = 'Completed'
            db.session.commit()
            
            return jsonify({
                'message': f'Session {session.session_code} completed successfully',
                'session': session.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
