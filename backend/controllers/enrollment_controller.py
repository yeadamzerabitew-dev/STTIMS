from flask import request, jsonify
from flask_login import login_required, current_user
from models import Trainee, Batch, Course, Enrollment
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime, date
import re

class EnrollmentController:
    """Controller for enrollment management operations"""
    
    @staticmethod
    def generate_enrollment_number():
        """Generate a unique enrollment number"""
        year = datetime.now().year
        count = Enrollment.query.count() + 1
        return f"E-{year}-{str(count).zfill(4)}"
    
    @staticmethod
    def calculate_final_amount(course_fee, discount_amount):
        """Calculate final amount after discount"""
        if discount_amount:
            return max(0, course_fee - discount_amount)
        return course_fee
    
    # =============================================
    # CREATE ENROLLMENT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def create_enrollment():
        """Create a new enrollment"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['trainee_id', 'batch_id']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate trainee
            trainee = Trainee.query.get(data['trainee_id'])
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 400
            if trainee.status != 'Active':
                return jsonify({'error': 'Trainee must be active'}), 400
            
            # Validate batch
            batch = Batch.query.get(data['batch_id'])
            if not batch:
                return jsonify({'error': 'Batch not found'}), 400
            
            # Check batch status
            if batch.status == 'Completed':
                return jsonify({'error': 'Cannot enroll in completed batch'}), 400
            if batch.status == 'Cancelled':
                return jsonify({'error': 'Cannot enroll in cancelled batch'}), 400
            if batch.status == 'Upcoming' and batch.start_date < date.today():
                # Auto-update status if batch should have started
                batch.status = 'Ongoing'
            
            # Check if course is active
            if batch.course.status != 'Active':
                return jsonify({'error': 'Course is not active'}), 400
            
            # Check capacity
            if (batch.current_enrollment or 0) >= batch.max_capacity:
                return jsonify({
                    'error': 'Batch is full',
                    'max_capacity': batch.max_capacity,
                    'current_enrollment': batch.current_enrollment
                }), 400
            
            # Check for duplicate enrollment
            existing = Enrollment.query.filter_by(
                trainee_id=data['trainee_id'],
                batch_id=data['batch_id']
            ).first()
            if existing:
                return jsonify({
                    'error': 'Trainee is already enrolled in this batch',
                    'enrollment_id': existing.enrollment_id,
                    'status': existing.status
                }), 400
            
            # Validate payment information
            payment_status = data.get('payment_status', 'Pending')
            valid_payment_statuses = ['Paid', 'Pending', 'Partial', 'Scholarship']
            if payment_status not in valid_payment_statuses:
                return jsonify({'error': 'Invalid payment status'}), 400
            
            # If payment status is 'Paid', payment amount is required
            payment_amount = data.get('payment_amount')
            if payment_status == 'Paid' and (payment_amount is None or payment_amount <= 0):
                return jsonify({'error': 'Payment amount is required for paid enrollment'}), 400
            
            # Validate payment method if payment is made
            if payment_amount and payment_amount > 0:
                payment_method = data.get('payment_method')
                if not payment_method:
                    return jsonify({'error': 'Payment method is required for payments'}), 400
            
            # Calculate final amount
            course_fee = batch.course.fee_amount
            discount_amount = data.get('discount_amount', 0)
            if discount_amount < 0:
                return jsonify({'error': 'Discount cannot be negative'}), 400
            if discount_amount > course_fee:
                return jsonify({'error': 'Discount cannot exceed course fee'}), 400
            
            final_amount = EnrollmentController.calculate_final_amount(course_fee, discount_amount)
            
            # Generate enrollment number
            enrollment_number = EnrollmentController.generate_enrollment_number()
            
            # Create enrollment
            enrollment = Enrollment(
                enrollment_number=enrollment_number,
                trainee_id=data['trainee_id'],
                batch_id=data['batch_id'],
                enrollment_date=date.today(),
                status='Enrolled',
                payment_status=payment_status,
                payment_amount=payment_amount,
                payment_date=date.today() if payment_amount and payment_amount > 0 else None,
                payment_method=data.get('payment_method') if payment_amount and payment_amount > 0 else None,
                discount_amount=discount_amount,
                final_amount=final_amount,
                notes=data.get('notes', '').strip() if data.get('notes') else None
            )
            
            db.session.add(enrollment)
            
            # Update batch enrollment count
            batch.current_enrollment = (batch.current_enrollment or 0) + 1
            
            db.session.commit()
            
            return jsonify({
                'message': 'Enrollment created successfully',
                'enrollment': enrollment.to_dict(),
                'batch': {
                    'current_enrollment': batch.current_enrollment,
                    'max_capacity': batch.max_capacity,
                    'available_slots': batch.max_capacity - batch.current_enrollment
                }
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # READ ENROLLMENTS (List with Search, Filter, Sort, Pagination)
    # =============================================
    
    @staticmethod
    @login_required
    def list_enrollments():
        """List all enrollments with search, filter, sort, and pagination"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            search = request.args.get('search', '')
            trainee_id = request.args.get('trainee_id', type=int)
            batch_id = request.args.get('batch_id', type=int)
            status = request.args.get('status', '')
            payment_status = request.args.get('payment_status', '')
            sort_by = request.args.get('sort_by', 'enrollment_date')
            sort_order = request.args.get('sort_order', 'desc')
            
            # Build query
            query = Enrollment.query
            
            # Apply search filter
            if search:
                query = query.join(Trainee).join(Batch).join(Course).filter(
                    (Trainee.first_name.ilike(f'%{search}%')) |
                    (Trainee.last_name.ilike(f'%{search}%')) |
                    (Trainee.trainee_code.ilike(f'%{search}%')) |
                    (Course.course_title.ilike(f'%{search}%')) |
                    (Batch.batch_name.ilike(f'%{search}%')) |
                    (Enrollment.enrollment_number.ilike(f'%{search}%'))
                )
            
            # Apply trainee filter
            if trainee_id:
                query = query.filter(Enrollment.trainee_id == trainee_id)
            
            # Apply batch filter
            if batch_id:
                query = query.filter(Enrollment.batch_id == batch_id)
            
            # Apply status filter
            if status:
                query = query.filter(Enrollment.status == status)
            
            # Apply payment status filter
            if payment_status:
                query = query.filter(Enrollment.payment_status == payment_status)
            
            # Apply sorting
            valid_sort_fields = ['enrollment_id', 'enrollment_number', 'enrollment_date', 
                                 'status', 'payment_status', 'final_amount']
            if sort_by in valid_sort_fields:
                if sort_order.lower() == 'asc':
                    query = query.order_by(getattr(Enrollment, sort_by).asc())
                else:
                    query = query.order_by(getattr(Enrollment, sort_by).desc())
            else:
                query = query.order_by(Enrollment.enrollment_date.desc())
            
            # Paginate
            enrollments = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'data': [enrollment.to_dict() for enrollment in enrollments.items],
                'total': enrollments.total,
                'page': enrollments.page,
                'per_page': enrollments.per_page,
                'total_pages': enrollments.pages,
                'has_prev': enrollments.has_prev,
                'has_next': enrollments.has_next,
                'filters': {
                    'search': search,
                    'trainee_id': trainee_id,
                    'batch_id': batch_id,
                    'status': status,
                    'payment_status': payment_status,
                    'sort_by': sort_by,
                    'sort_order': sort_order
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # READ SINGLE ENROLLMENT
    # =============================================
    
    @staticmethod
    @login_required
    def get_enrollment(enrollment_id):
        """Get enrollment details by ID"""
        try:
            enrollment = Enrollment.query.get(enrollment_id)
            if not enrollment:
                return jsonify({'error': 'Enrollment not found'}), 404
            
            # Get related info
            trainee = Trainee.query.get(enrollment.trainee_id)
            batch = Batch.query.get(enrollment.batch_id)
            course = Course.query.get(batch.course_id) if batch else None
            
            return jsonify({
                'enrollment': enrollment.to_dict(),
                'trainee': trainee.to_dict_minimal() if trainee else None,
                'batch': batch.to_dict_minimal() if batch else None,
                'course': course.to_dict_minimal() if course else None
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # UPDATE ENROLLMENT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def update_enrollment(enrollment_id):
        """Update an existing enrollment"""
        try:
            enrollment = Enrollment.query.get(enrollment_id)
            if not enrollment:
                return jsonify({'error': 'Enrollment not found'}), 404
            
            data = request.get_json()
            
            # Update status
            if data.get('status'):
                valid_statuses = ['Enrolled', 'Active', 'Completed', 'Dropped', 'Suspended']
                if data['status'] not in valid_statuses:
                    return jsonify({'error': 'Invalid status'}), 400
                
                # If status is Completed, update completion date
                if data['status'] == 'Completed':
                    enrollment.completion_date = date.today()
                
                # If status is Dropped, update drop date
                if data['status'] == 'Dropped':
                    enrollment.drop_date = date.today()
                    # Update batch enrollment count
                    batch = Batch.query.get(enrollment.batch_id)
                    if batch and (batch.current_enrollment or 0) > 0:
                        batch.current_enrollment = (batch.current_enrollment or 0) - 1
                
                enrollment.status = data['status']
            
            # Update payment status
            if data.get('payment_status'):
                valid_payment_statuses = ['Paid', 'Pending', 'Partial', 'Scholarship']
                if data['payment_status'] not in valid_payment_statuses:
                    return jsonify({'error': 'Invalid payment status'}), 400
                enrollment.payment_status = data['payment_status']
            
            # Update payment amount
            if data.get('payment_amount') is not None:
                if data['payment_amount'] < 0:
                    return jsonify({'error': 'Payment amount cannot be negative'}), 400
                enrollment.payment_amount = data['payment_amount']
                if data['payment_amount'] > 0:
                    enrollment.payment_date = date.today()
            
            # Update payment method
            if data.get('payment_method') is not None:
                enrollment.payment_method = data['payment_method'].strip() if data['payment_method'] else None
            
            # Update discount amount
            if data.get('discount_amount') is not None:
                if data['discount_amount'] < 0:
                    return jsonify({'error': 'Discount cannot be negative'}), 400
                if data['discount_amount'] > enrollment.batch.course.fee_amount:
                    return jsonify({'error': 'Discount cannot exceed course fee'}), 400
                enrollment.discount_amount = data['discount_amount']
                enrollment.final_amount = EnrollmentController.calculate_final_amount(
                    enrollment.batch.course.fee_amount,
                    data['discount_amount']
                )
            
            # Update grade
            if data.get('grade') is not None:
                enrollment.grade = data['grade'].upper() if data['grade'] else None
            
            # Update performance summary
            if data.get('performance_summary') is not None:
                enrollment.performance_summary = data['performance_summary'].strip() if data['performance_summary'] else None
            
            # Update notes
            if data.get('notes') is not None:
                enrollment.notes = data['notes'].strip() if data['notes'] else None
            
            db.session.commit()
            
            return jsonify({
                'message': 'Enrollment updated successfully',
                'enrollment': enrollment.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # DROP ENROLLMENT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def drop_enrollment(enrollment_id):
        """Drop an enrollment"""
        try:
            enrollment = Enrollment.query.get(enrollment_id)
            if not enrollment:
                return jsonify({'error': 'Enrollment not found'}), 404
            
            if enrollment.status == 'Dropped':
                return jsonify({'error': 'Enrollment is already dropped'}), 400
            
            if enrollment.status == 'Completed':
                return jsonify({'error': 'Cannot drop a completed enrollment'}), 400
            
            data = request.get_json(silent=True) or {}
            
            enrollment.status = 'Dropped'
            enrollment.drop_date = date.today()
            enrollment.drop_reason = data.get('reason', '').strip() if data.get('reason') else None
            
            # Update batch enrollment count
            batch = Batch.query.get(enrollment.batch_id)
            if batch and batch.current_enrollment > 0:
                batch.current_enrollment -= 1
            
            db.session.commit()
            
            return jsonify({
                'message': 'Enrollment dropped successfully',
                'enrollment': enrollment.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # COMPLETE ENROLLMENT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def complete_enrollment(enrollment_id):
        """Mark enrollment as completed"""
        try:
            enrollment = Enrollment.query.get(enrollment_id)
            if not enrollment:
                return jsonify({'error': 'Enrollment not found'}), 404
            
            if enrollment.status == 'Completed':
                return jsonify({'error': 'Enrollment is already completed'}), 400
            
            # Check if attendance is sufficient
            if (enrollment.attendance_percentage or 0) < 75:
                return jsonify({
                    'error': f'Attendance is {enrollment.attendance_percentage}%. Minimum 75% required for completion'
                }), 400
            
            enrollment.status = 'Completed'
            enrollment.completion_date = date.today()
            enrollment.completion_percentage = 100
            
            db.session.commit()
            
            return jsonify({
                'message': 'Enrollment completed successfully',
                'enrollment': enrollment.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # PROCESS PAYMENT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def process_payment(enrollment_id):
        """Process a payment for an enrollment"""
        try:
            enrollment = Enrollment.query.get(enrollment_id)
            if not enrollment:
                return jsonify({'error': 'Enrollment not found'}), 404
            
            data = request.get_json()
            
            if not data.get('amount'):
                return jsonify({'error': 'Payment amount is required'}), 400
            
            if data['amount'] <= 0:
                return jsonify({'error': 'Payment amount must be positive'}), 400
            
            # Calculate remaining balance
            remaining = enrollment.final_amount - (enrollment.payment_amount or 0)
            if data['amount'] > remaining:
                return jsonify({
                    'error': f'Payment amount exceeds remaining balance ({remaining})',
                    'remaining_balance': remaining
                }), 400
            
            # Update payment
            if enrollment.payment_amount is None:
                enrollment.payment_amount = 0
            enrollment.payment_amount += data['amount']
            enrollment.payment_date = date.today()
            
            if data.get('payment_method'):
                enrollment.payment_method = data['payment_method']
            
            # Update payment status
            if enrollment.payment_amount >= enrollment.final_amount:
                enrollment.payment_status = 'Paid'
            else:
                enrollment.payment_status = 'Partial'
            
            db.session.commit()
            
            return jsonify({
                'message': 'Payment processed successfully',
                'enrollment': enrollment.to_dict(),
                'remaining_balance': enrollment.final_amount - enrollment.payment_amount
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET ENROLLMENT STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_enrollment_stats():
        """Get enrollment statistics"""
        try:
            total = Enrollment.query.count()
            active = Enrollment.query.filter_by(status='Active').count()
            enrolled = Enrollment.query.filter_by(status='Enrolled').count()
            completed = Enrollment.query.filter_by(status='Completed').count()
            dropped = Enrollment.query.filter_by(status='Dropped').count()
            suspended = Enrollment.query.filter_by(status='Suspended').count()
            
            # Payment status breakdown
            payment_stats = {}
            statuses = ['Paid', 'Pending', 'Partial', 'Scholarship']
            for pstatus in statuses:
                payment_stats[pstatus] = Enrollment.query.filter_by(payment_status=pstatus).count()
            
            # Revenue statistics
            total_revenue = db.session.query(db.func.sum(Enrollment.payment_amount)).scalar() or 0
            total_expected = db.session.query(db.func.sum(Enrollment.final_amount)).scalar() or 0
            total_discounts = db.session.query(db.func.sum(Enrollment.discount_amount)).scalar() or 0
            
            return jsonify({
                'total_enrollments': total,
                'active_enrollments': active,
                'enrolled_enrollments': enrolled,
                'completed_enrollments': completed,
                'dropped_enrollments': dropped,
                'suspended_enrollments': suspended,
                'payment_breakdown': payment_stats,
                'revenue': {
                    'total_revenue': float(total_revenue),
                    'total_expected': float(total_expected),
                    'total_discounts': float(total_discounts),
                    'pending_amount': float(total_expected - total_revenue)
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
