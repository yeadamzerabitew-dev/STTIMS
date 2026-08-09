from flask import request, jsonify
from flask_login import login_required, current_user
from models import Batch, Course, Instructor
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime, date
import re

class BatchController:
    """Controller for batch management operations"""
    
    @staticmethod
    def validate_batch_code(code):
        """Validate batch code (alphanumeric, 3-20 chars)"""
        pattern = r'^[A-Z0-9\-]{3,20}$'
        return re.match(pattern, code.upper()) is not None
    
    @staticmethod
    def generate_batch_code(course_code, batch_number):
        """Generate a batch code"""
        year = datetime.now().year
        return f"{course_code}-{year}-{str(batch_number).zfill(3)}"
    
    # =============================================
    # CREATE BATCH
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def create_batch():
        """Create a new batch"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['course_id', 'batch_name', 'start_date', 'end_date', 'schedule_type', 'max_capacity']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate course
            course = Course.query.get(data['course_id'])
            if not course:
                return jsonify({'error': 'Course not found'}), 400
            if course.status != 'Active':
                return jsonify({'error': 'Course must be active'}), 400
            
            # Validate dates
            try:
                start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
                end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
                
                if start_date >= end_date:
                    return jsonify({'error': 'End date must be after start date'}), 400
                
                if start_date < date.today():
                    return jsonify({'error': 'Start date cannot be in the past'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
            # Validate schedule type
            valid_schedule_types = ['Weekday', 'Weekend', 'Evening', 'Intensive']
            if data['schedule_type'] not in valid_schedule_types:
                return jsonify({'error': 'Invalid schedule type'}), 400
            
            # Validate capacity
            if data['max_capacity'] <= 0:
                return jsonify({'error': 'Maximum capacity must be greater than 0'}), 400
            
            # Validate minimum trainees
            min_trainees = data.get('min_trainees_required', 5)
            if min_trainees < 0:
                return jsonify({'error': 'Minimum trainees cannot be negative'}), 400
            if min_trainees > data['max_capacity']:
                return jsonify({'error': 'Minimum trainees cannot exceed maximum capacity'}), 400
            
            # Validate instructor if provided
            instructor_id = data.get('instructor_id')
            if instructor_id:
                instructor = Instructor.query.get(instructor_id)
                if not instructor:
                    return jsonify({'error': 'Instructor not found'}), 400
                if instructor.status != 'Active':
                    return jsonify({'error': 'Instructor must be active'}), 400
                
                # Check if instructor is available during the batch period
                if not BatchController._check_instructor_availability(instructor_id, start_date, end_date):
                    return jsonify({'error': 'Instructor is not available during this period'}), 400
            
            # Generate batch code
            batch_count = Batch.query.filter_by(course_id=data['course_id']).count() + 1
            batch_code = BatchController.generate_batch_code(course.course_code, batch_count)
            
            # Create batch
            batch = Batch(
                batch_code=batch_code,
                batch_name=data['batch_name'].strip(),
                course_id=data['course_id'],
                start_date=start_date,
                end_date=end_date,
                schedule_type=data['schedule_type'],
                schedule_days=data.get('schedule_days', '').strip() if data.get('schedule_days') else None,
                schedule_time=data.get('schedule_time'),
                schedule_end_time=data.get('schedule_end_time'),
                room_number=data.get('room_number', '').strip() if data.get('room_number') else None,
                building=data.get('building', '').strip() if data.get('building') else None,
                max_capacity=data['max_capacity'],
                min_trainees_required=min_trainees,
                instructor_id=instructor_id,
                status='Upcoming',
                notes=data.get('notes', '').strip() if data.get('notes') else None
            )
            
            db.session.add(batch)
            db.session.commit()
            
            return jsonify({
                'message': 'Batch created successfully',
                'batch': batch.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    def _check_instructor_availability(instructor_id, start_date, end_date):
        """Check if instructor is available during the given period"""
        # Get all active assignments for this instructor
        from models import CourseAssignment
        assignments = CourseAssignment.query.filter_by(
            instructor_id=instructor_id,
            status='Active'
        ).all()
        
        for assignment in assignments:
            batch = Batch.query.get(assignment.batch_id)
            if batch:
                # Check if dates overlap
                if not (end_date < batch.start_date or start_date > batch.end_date):
                    return False
        return True
    
    # =============================================
    # READ BATCHES (List with Search, Filter, Sort, Pagination)
    # =============================================
    
    @staticmethod
    @login_required
    def list_batches():
        """List all batches with search, filter, sort, and pagination"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            search = request.args.get('search', '')
            course_id = request.args.get('course_id', type=int)
            instructor_id = request.args.get('instructor_id', type=int)
            status = request.args.get('status', '')
            schedule_type = request.args.get('schedule_type', '')
            start_date_from = request.args.get('start_date_from')
            start_date_to = request.args.get('start_date_to')
            sort_by = request.args.get('sort_by', 'start_date')
            sort_order = request.args.get('sort_order', 'asc')
            
            # Build query
            query = Batch.query
            
            # Apply search filter
            if search:
                query = query.filter(
                    (Batch.batch_name.ilike(f'%{search}%')) |
                    (Batch.batch_code.ilike(f'%{search}%')) |
                    (Batch.room_number.ilike(f'%{search}%'))
                )
            
            # Apply course filter
            if course_id:
                query = query.filter(Batch.course_id == course_id)
            
            # Apply instructor filter
            if instructor_id:
                query = query.filter(Batch.instructor_id == instructor_id)
            
            # Apply status filter
            if status:
                query = query.filter(Batch.status == status)
            
            # Apply schedule type filter
            if schedule_type:
                query = query.filter(Batch.schedule_type == schedule_type)
            
            # Apply date range filter
            if start_date_from:
                try:
                    from_date = datetime.strptime(start_date_from, '%Y-%m-%d').date()
                    query = query.filter(Batch.start_date >= from_date)
                except ValueError:
                    pass
            
            if start_date_to:
                try:
                    to_date = datetime.strptime(start_date_to, '%Y-%m-%d').date()
                    query = query.filter(Batch.start_date <= to_date)
                except ValueError:
                    pass
            
            # Apply sorting
            valid_sort_fields = ['batch_id', 'batch_code', 'batch_name', 'start_date', 
                                 'end_date', 'max_capacity', 'current_enrollment', 'status']
            if sort_by in valid_sort_fields:
                if sort_order.lower() == 'asc':
                    query = query.order_by(getattr(Batch, sort_by).asc())
                else:
                    query = query.order_by(getattr(Batch, sort_by).desc())
            else:
                query = query.order_by(Batch.start_date.asc())
            
            # Paginate
            batches = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'data': [batch.to_dict() for batch in batches.items],
                'total': batches.total,
                'page': batches.page,
                'per_page': batches.per_page,
                'total_pages': batches.pages,
                'has_prev': batches.has_prev,
                'has_next': batches.has_next,
                'filters': {
                    'search': search,
                    'course_id': course_id,
                    'instructor_id': instructor_id,
                    'status': status,
                    'schedule_type': schedule_type,
                    'start_date_from': start_date_from,
                    'start_date_to': start_date_to,
                    'sort_by': sort_by,
                    'sort_order': sort_order
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # READ SINGLE BATCH
    # =============================================
    
    @staticmethod
    @login_required
    def get_batch(batch_id):
        """Get batch details by ID"""
        try:
            batch = Batch.query.get(batch_id)
            if not batch:
                return jsonify({'error': 'Batch not found'}), 404
            
            # Get related info
            course = Course.query.get(batch.course_id)
            instructor = Instructor.query.get(batch.instructor_id) if batch.instructor_id else None
            
            # Get enrollment statistics
            enrollments = batch.enrollments
            total_enrolled = enrollments.count()
            active_enrollments = enrollments.filter_by(status='Active').count()
            completed_enrollments = enrollments.filter_by(status='Completed').count()
            
            # Get class sessions count
            sessions_count = batch.sessions.count()
            
            return jsonify({
                'batch': batch.to_dict(),
                'course': course.to_dict_minimal() if course else None,
                'instructor': instructor.to_dict_minimal() if instructor else None,
                'statistics': {
                    'total_enrolled': total_enrolled,
                    'active_enrollments': active_enrollments,
                    'completed_enrollments': completed_enrollments,
                    'sessions_count': sessions_count,
                    'capacity_utilization': round((total_enrolled / batch.max_capacity) * 100, 2) if batch.max_capacity > 0 else 0
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # UPDATE BATCH
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def update_batch(batch_id):
        """Update an existing batch"""
        try:
            batch = Batch.query.get(batch_id)
            if not batch:
                return jsonify({'error': 'Batch not found'}), 404
            
            # Cannot update completed or cancelled batches
            if batch.status in ['Completed', 'Cancelled']:
                return jsonify({'error': f'Cannot update {batch.status.lower()} batch'}), 400
            
            data = request.get_json()
            
            # Update batch name
            if data.get('batch_name'):
                batch.batch_name = data['batch_name'].strip()
            
            # Update dates (if batch is not started)
            if batch.status == 'Upcoming':
                if data.get('start_date'):
                    try:
                        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
                        if start_date < date.today():
                            return jsonify({'error': 'Start date cannot be in the past'}), 400
                        batch.start_date = start_date
                    except ValueError:
                        return jsonify({'error': 'Invalid start date format'}), 400
                
                if data.get('end_date'):
                    try:
                        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
                        if end_date <= batch.start_date:
                            return jsonify({'error': 'End date must be after start date'}), 400
                        batch.end_date = end_date
                    except ValueError:
                        return jsonify({'error': 'Invalid end date format'}), 400
            
            # Update schedule
            if data.get('schedule_type'):
                valid_schedule_types = ['Weekday', 'Weekend', 'Evening', 'Intensive']
                if data['schedule_type'] not in valid_schedule_types:
                    return jsonify({'error': 'Invalid schedule type'}), 400
                batch.schedule_type = data['schedule_type']
            
            if data.get('schedule_days') is not None:
                batch.schedule_days = data['schedule_days'].strip() if data['schedule_days'] else None
            
            if data.get('schedule_time'):
                batch.schedule_time = data['schedule_time']
            
            if data.get('schedule_end_time'):
                batch.schedule_end_time = data['schedule_end_time']
            
            # Update room
            if data.get('room_number') is not None:
                batch.room_number = data['room_number'].strip() if data['room_number'] else None
            
            if data.get('building') is not None:
                batch.building = data['building'].strip() if data['building'] else None
            
            # Update capacity (cannot reduce below current enrollment)
            if data.get('max_capacity'):
                if data['max_capacity'] <= 0:
                    return jsonify({'error': 'Maximum capacity must be greater than 0'}), 400
                if data['max_capacity'] < batch.current_enrollment:
                    return jsonify({'error': f'Capacity cannot be less than current enrollment ({batch.current_enrollment})'}), 400
                batch.max_capacity = data['max_capacity']
            
            # Update min trainees
            if data.get('min_trainees_required') is not None:
                if data['min_trainees_required'] < 0:
                    return jsonify({'error': 'Minimum trainees cannot be negative'}), 400
                if data['min_trainees_required'] > batch.max_capacity:
                    return jsonify({'error': 'Minimum trainees cannot exceed maximum capacity'}), 400
                batch.min_trainees_required = data['min_trainees_required']
            
            # Update instructor
            if 'instructor_id' in data:
                if data['instructor_id'] is None:
                    batch.instructor_id = None
                else:
                    instructor = Instructor.query.get(data['instructor_id'])
                    if not instructor:
                        return jsonify({'error': 'Instructor not found'}), 400
                    if instructor.status != 'Active':
                        return jsonify({'error': 'Instructor must be active'}), 400
                    
                    # Check availability
                    if not BatchController._check_instructor_availability(data['instructor_id'], batch.start_date, batch.end_date):
                        return jsonify({'error': 'Instructor is not available during this period'}), 400
                    
                    batch.instructor_id = data['instructor_id']
            
            # Update status (only if not completed or cancelled)
            if data.get('status'):
                valid_statuses = ['Upcoming', 'Ongoing']
                if batch.status in ['Completed', 'Cancelled']:
                    return jsonify({'error': 'Cannot change status of completed/cancelled batch'}), 400
                if data['status'] not in valid_statuses:
                    return jsonify({'error': 'Invalid status'}), 400
                batch.status = data['status']
            
            # Update notes
            if data.get('notes') is not None:
                batch.notes = data['notes'].strip() if data['notes'] else None
            
            db.session.commit()
            
            return jsonify({
                'message': 'Batch updated successfully',
                'batch': batch.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # CLOSE BATCH (Mark as Completed)
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def close_batch(batch_id):
        """Close a batch (mark as Completed)"""
        try:
            batch = Batch.query.get(batch_id)
            if not batch:
                return jsonify({'error': 'Batch not found'}), 404
            
            if batch.status == 'Completed':
                return jsonify({'error': 'Batch is already completed'}), 400
            
            if batch.status == 'Cancelled':
                return jsonify({'error': 'Cannot close a cancelled batch'}), 400
            
            # Check if batch has minimum required trainees
            if batch.current_enrollment < batch.min_trainees_required:
                return jsonify({
                    'error': f'Batch has only {batch.current_enrollment} trainees. Minimum required: {batch.min_trainees_required}'
                }), 400
            
            batch.status = 'Completed'
            db.session.commit()
            
            return jsonify({
                'message': f'Batch "{batch.batch_name}" closed successfully',
                'batch': batch.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # CANCEL BATCH
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def cancel_batch(batch_id):
        """Cancel a batch"""
        try:
            batch = Batch.query.get(batch_id)
            if not batch:
                return jsonify({'error': 'Batch not found'}), 404
            
            if batch.status == 'Completed':
                return jsonify({'error': 'Cannot cancel a completed batch'}), 400
            
            if batch.status == 'Cancelled':
                return jsonify({'error': 'Batch is already cancelled'}), 400
            
            batch.status = 'Cancelled'
            db.session.commit()
            
            return jsonify({
                'message': f'Batch "{batch.batch_name}" cancelled successfully',
                'batch': batch.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # START BATCH (Mark as Ongoing)
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def start_batch(batch_id):
        """Start a batch (mark as Ongoing)"""
        try:
            batch = Batch.query.get(batch_id)
            if not batch:
                return jsonify({'error': 'Batch not found'}), 404
            
            if batch.status == 'Ongoing':
                return jsonify({'error': 'Batch is already ongoing'}), 400
            
            if batch.status == 'Completed':
                return jsonify({'error': 'Cannot start a completed batch'}), 400
            
            if batch.status == 'Cancelled':
                return jsonify({'error': 'Cannot start a cancelled batch'}), 400
            
            # Check if today is within the batch date range
            today = date.today()
            if today < batch.start_date:
                return jsonify({'error': f'Batch starts on {batch.start_date}. Cannot start early.'}), 400
            if today > batch.end_date:
                return jsonify({'error': f'Batch ended on {batch.end_date}. Cannot start.'}), 400
            
            # Check if minimum required trainees
            if batch.current_enrollment < batch.min_trainees_required:
                return jsonify({
                    'error': f'Batch has only {batch.current_enrollment} trainees. Minimum required: {batch.min_trainees_required}'
                }), 400
            
            batch.status = 'Ongoing'
            db.session.commit()
            
            return jsonify({
                'message': f'Batch "{batch.batch_name}" started successfully',
                'batch': batch.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET BATCH STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_batch_stats():
        """Get batch statistics"""
        try:
            total = Batch.query.count()
            upcoming = Batch.query.filter_by(status='Upcoming').count()
            ongoing = Batch.query.filter_by(status='Ongoing').count()
            completed = Batch.query.filter_by(status='Completed').count()
            cancelled = Batch.query.filter_by(status='Cancelled').count()
            
            # Schedule type breakdown
            schedule_stats = {}
            types = ['Weekday', 'Weekend', 'Evening', 'Intensive']
            for stype in types:
                schedule_stats[stype] = Batch.query.filter_by(schedule_type=stype).count()
            
            # Capacity utilization
            total_capacity = db.session.query(db.func.sum(Batch.max_capacity)).scalar() or 0
            total_enrollment = db.session.query(db.func.sum(Batch.current_enrollment)).scalar() or 0
            
            return jsonify({
                'total_batches': total,
                'upcoming_batches': upcoming,
                'ongoing_batches': ongoing,
                'completed_batches': completed,
                'cancelled_batches': cancelled,
                'schedule_breakdown': schedule_stats,
                'capacity_utilization': {
                    'total_capacity': total_capacity,
                    'total_enrollment': total_enrollment,
                    'utilization_rate': round((total_enrollment / total_capacity) * 100, 2) if total_capacity > 0 else 0
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
