from flask import request, jsonify
from flask_login import login_required, current_user
from models import Course, Category
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime
import re

class CourseController:
    """Controller for course management operations"""
    
    @staticmethod
    def validate_course_code(code):
        """Validate course code (alphanumeric, 3-20 chars)"""
        pattern = r'^[A-Z0-9]{3,20}$'
        return re.match(pattern, code.upper()) is not None
    
    @staticmethod
    def generate_course_code(title):
        """Generate a course code from title"""
        # Take first 3 letters of each word, join, add random number
        words = title.split()
        code = ''.join([word[:3].upper() for word in words[:3]])
        # If code is too short, pad with 'X'
        while len(code) < 3:
            code += 'X'
        # Add a random number to ensure uniqueness
        import random
        code += str(random.randint(10, 99))
        return code
    
    # =============================================
    # CREATE COURSE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def create_course():
        """Create a new course"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['course_title', 'category_id', 'duration_hours', 'fee_amount', 'max_capacity']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate course code (auto-generate if not provided)
            if data.get('course_code'):
                if not CourseController.validate_course_code(data['course_code']):
                    return jsonify({'error': 'Course code must be 3-20 alphanumeric characters'}), 400
                course_code = data['course_code'].upper()
                if Course.query.filter_by(course_code=course_code).first():
                    return jsonify({'error': 'Course code already exists'}), 400
            else:
                # Auto-generate course code
                course_code = CourseController.generate_course_code(data['course_title'])
                # Ensure uniqueness
                attempt = 0
                while Course.query.filter_by(course_code=course_code).first():
                    course_code = CourseController.generate_course_code(data['course_title'] + str(attempt))
                    attempt += 1
            
            # Validate category
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({'error': 'Category not found'}), 400
            if category.status != 'Active':
                return jsonify({'error': 'Category must be active'}), 400
            
            # Validate duration
            if data['duration_hours'] <= 0:
                return jsonify({'error': 'Duration hours must be positive'}), 400
            
            # Validate fee
            if data['fee_amount'] < 0:
                return jsonify({'error': 'Fee amount cannot be negative'}), 400
            
            # Validate capacity
            if data['max_capacity'] <= 0:
                return jsonify({'error': 'Maximum capacity must be greater than 0'}), 400
            
            # Validate level
            valid_levels = ['Beginner', 'Intermediate', 'Advanced']
            if data.get('course_level') and data['course_level'] not in valid_levels:
                return jsonify({'error': 'Invalid course level'}), 400
            
            # Create course
            course = Course(
                course_code=course_code,
                course_title=data['course_title'].strip(),
                category_id=data['category_id'],
                description=data.get('description', '').strip() if data.get('description') else None,
                learning_objectives=data.get('learning_objectives', '').strip() if data.get('learning_objectives') else None,
                prerequisites=data.get('prerequisites', '').strip() if data.get('prerequisites') else None,
                duration_hours=data['duration_hours'],
                duration_weeks=data.get('duration_weeks'),
                fee_amount=data['fee_amount'],
                fee_currency=data.get('fee_currency', 'ETB'),
                min_age_requirement=data.get('min_age_requirement'),
                max_capacity=data['max_capacity'],
                course_level=data.get('course_level', 'Beginner'),
                certification_available=data.get('certification_available', True),
                status='Active'
            )
            
            db.session.add(course)
            db.session.commit()
            
            return jsonify({
                'message': 'Course created successfully',
                'course': course.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # READ COURSES (List with Search, Filter, Sort, Pagination)
    # =============================================
    
    @staticmethod
    @login_required
    def list_courses():
        """List all courses with search, filter, sort, and pagination"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            search = request.args.get('search', '')
            category_id = request.args.get('category_id', type=int)
            level = request.args.get('level', '')
            status = request.args.get('status', '')
            min_fee = request.args.get('min_fee', type=float)
            max_fee = request.args.get('max_fee', type=float)
            sort_by = request.args.get('sort_by', 'created_at')
            sort_order = request.args.get('sort_order', 'desc')
            
            # Build query
            query = Course.query
            
            # Apply search filter
            if search:
                query = query.filter(
                    (Course.course_title.ilike(f'%{search}%')) |
                    (Course.course_code.ilike(f'%{search}%')) |
                    (Course.description.ilike(f'%{search}%'))
                )
            
            # Apply category filter
            if category_id:
                query = query.filter(Course.category_id == category_id)
            
            # Apply level filter
            if level:
                query = query.filter(Course.course_level == level)
            
            # Apply status filter
            if status:
                query = query.filter(Course.status == status)
            else:
                # Default: exclude archived unless specifically requested
                query = query.filter(Course.status != 'Archived')
            
            # Apply fee range filter
            if min_fee is not None:
                query = query.filter(Course.fee_amount >= min_fee)
            if max_fee is not None:
                query = query.filter(Course.fee_amount <= max_fee)
            
            # Apply sorting
            valid_sort_fields = ['course_id', 'course_code', 'course_title', 'duration_hours', 
                                 'fee_amount', 'max_capacity', 'course_level', 'created_at', 'status']
            if sort_by in valid_sort_fields:
                if sort_order.lower() == 'asc':
                    query = query.order_by(getattr(Course, sort_by).asc())
                else:
                    query = query.order_by(getattr(Course, sort_by).desc())
            else:
                query = query.order_by(Course.created_at.desc())
            
            # Paginate
            courses = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'data': [course.to_dict() for course in courses.items],
                'total': courses.total,
                'page': courses.page,
                'per_page': courses.per_page,
                'total_pages': courses.pages,
                'has_prev': courses.has_prev,
                'has_next': courses.has_next,
                'filters': {
                    'search': search,
                    'category_id': category_id,
                    'level': level,
                    'status': status,
                    'min_fee': min_fee,
                    'max_fee': max_fee,
                    'sort_by': sort_by,
                    'sort_order': sort_order
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # READ SINGLE COURSE
    # =============================================
    
    @staticmethod
    @login_required
    def get_course(course_id):
        """Get course details by ID"""
        try:
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': 'Course not found'}), 404
            
            # Get category info
            category = Category.query.get(course.category_id)
            
            # Get batch count
            batch_count = course.batches.count()
            
            # Get enrollment statistics
            from models import Enrollment, Batch
            total_enrollments = Enrollment.query.join(Batch).filter(
                Batch.course_id == course_id
            ).count()
            
            return jsonify({
                'course': course.to_dict(),
                'category': category.to_dict_minimal() if category else None,
                'batch_count': batch_count,
                'total_enrollments': total_enrollments
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # UPDATE COURSE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def update_course(course_id):
        """Update an existing course"""
        try:
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': 'Course not found'}), 404
            
            data = request.get_json()
            
            # Update course code (with validation)
            if data.get('course_code'):
                if not CourseController.validate_course_code(data['course_code']):
                    return jsonify({'error': 'Course code must be 3-20 alphanumeric characters'}), 400
                existing = Course.query.filter_by(course_code=data['course_code'].upper()).first()
                if existing and existing.course_id != course_id:
                    return jsonify({'error': 'Course code already exists'}), 400
                course.course_code = data['course_code'].upper()
            
            # Update course title
            if data.get('course_title'):
                course.course_title = data['course_title'].strip()
            
            # Update category
            if data.get('category_id'):
                category = Category.query.get(data['category_id'])
                if not category:
                    return jsonify({'error': 'Category not found'}), 400
                if category.status != 'Active':
                    return jsonify({'error': 'Category must be active'}), 400
                course.category_id = data['category_id']
            
            # Update description and objectives
            if data.get('description') is not None:
                course.description = data['description'].strip() if data['description'] else None
            
            if data.get('learning_objectives') is not None:
                course.learning_objectives = data['learning_objectives'].strip() if data['learning_objectives'] else None
            
            if data.get('prerequisites') is not None:
                course.prerequisites = data['prerequisites'].strip() if data['prerequisites'] else None
            
            # Update duration
            if data.get('duration_hours'):
                if data['duration_hours'] <= 0:
                    return jsonify({'error': 'Duration hours must be positive'}), 400
                course.duration_hours = data['duration_hours']
            
            if data.get('duration_weeks') is not None:
                if data['duration_weeks'] is not None and data['duration_weeks'] < 0:
                    return jsonify({'error': 'Duration weeks cannot be negative'}), 400
                course.duration_weeks = data['duration_weeks']
            
            # Update fee
            if data.get('fee_amount') is not None:
                if data['fee_amount'] < 0:
                    return jsonify({'error': 'Fee amount cannot be negative'}), 400
                course.fee_amount = data['fee_amount']
            
            if data.get('fee_currency'):
                course.fee_currency = data['fee_currency']
            
            # Update capacity
            if data.get('max_capacity'):
                if data['max_capacity'] <= 0:
                    return jsonify({'error': 'Maximum capacity must be greater than 0'}), 400
                course.max_capacity = data['max_capacity']
            
            # Update level
            if data.get('course_level'):
                valid_levels = ['Beginner', 'Intermediate', 'Advanced']
                if data['course_level'] not in valid_levels:
                    return jsonify({'error': 'Invalid course level'}), 400
                course.course_level = data['course_level']
            
            # Update certification availability
            if data.get('certification_available') is not None:
                course.certification_available = data['certification_available']
            
            # Update age requirement
            if data.get('min_age_requirement') is not None:
                if data['min_age_requirement'] is not None and data['min_age_requirement'] < 0:
                    return jsonify({'error': 'Age requirement cannot be negative'}), 400
                course.min_age_requirement = data['min_age_requirement']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Course updated successfully',
                'course': course.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # ARCHIVE COURSE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def archive_course(course_id):
        """Archive a course (set status to Archived)"""
        try:
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': 'Course not found'}), 404
            
            if course.status == 'Archived':
                return jsonify({'error': 'Course is already archived'}), 400
            
            # Check if course has active batches
            if course.batches.filter_by(status='Ongoing').count() > 0:
                return jsonify({'error': 'Cannot archive course with ongoing batches'}), 400
            
            course.status = 'Archived'
            db.session.commit()
            
            return jsonify({
                'message': f'Course "{course.course_title}" archived successfully',
                'course': course.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # ACTIVATE COURSE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def activate_course(course_id):
        """Activate a course (set status to Active)"""
        try:
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': 'Course not found'}), 404
            
            if course.status == 'Active':
                return jsonify({'error': 'Course is already active'}), 400
            
            course.status = 'Active'
            db.session.commit()
            
            return jsonify({
                'message': f'Course "{course.course_title}" activated successfully',
                'course': course.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # DELETE COURSE (Permanent)
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin'])
    def delete_course(course_id):
        """Permanently delete a course"""
        try:
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': 'Course not found'}), 404
            
            # Check if course has batches
            if course.batches.count() > 0:
                return jsonify({'error': 'Cannot delete course with existing batches'}), 400
            
            course_title = course.course_title
            db.session.delete(course)
            db.session.commit()
            
            return jsonify({
                'message': f'Course "{course_title}" deleted permanently'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET COURSE STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_course_stats():
        """Get course statistics"""
        try:
            total = Course.query.count()
            active = Course.query.filter_by(status='Active').count()
            inactive = Course.query.filter_by(status='Inactive').count()
            archived = Course.query.filter_by(status='Archived').count()
            
            # Level breakdown
            level_stats = {}
            levels = ['Beginner', 'Intermediate', 'Advanced']
            for level in levels:
                level_stats[level] = Course.query.filter_by(course_level=level).count()
            
            # Fee range breakdown
            fee_0_500 = Course.query.filter(Course.fee_amount.between(0, 500)).count()
            fee_501_1000 = Course.query.filter(Course.fee_amount.between(501, 1000)).count()
            fee_1001_2000 = Course.query.filter(Course.fee_amount.between(1001, 2000)).count()
            fee_2000_plus = Course.query.filter(Course.fee_amount > 2000).count()
            
            # Certification availability
            certification_available = Course.query.filter_by(certification_available=True).count()
            certification_not_available = Course.query.filter_by(certification_available=False).count()
            
            return jsonify({
                'total_courses': total,
                'active_courses': active,
                'inactive_courses': inactive,
                'archived_courses': archived,
                'level_breakdown': level_stats,
                'fee_breakdown': {
                    '0-500 ETB': fee_0_500,
                    '501-1000 ETB': fee_501_1000,
                    '1001-2000 ETB': fee_1001_2000,
                    '2000+ ETB': fee_2000_plus
                },
                'certification_available': certification_available,
                'certification_not_available': certification_not_available
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET COURSES BY CATEGORY
    # =============================================
    
    @staticmethod
    @login_required
    def get_courses_by_category(category_id):
        """Get all courses in a category"""
        try:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': 'Category not found'}), 404
            
            courses = Course.query.filter_by(
                category_id=category_id,
                status='Active'
            ).order_by(Course.course_title).all()
            
            return jsonify({
                'category': category.to_dict_minimal(),
                'courses': [course.to_dict_minimal() for course in courses]
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
