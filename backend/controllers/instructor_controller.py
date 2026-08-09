from flask import request, jsonify
from flask_login import login_required, current_user
from models import Instructor, InstructorSpecialization, User
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime, date
import re
import os
from werkzeug.utils import secure_filename

class InstructorController:
    """Controller for instructor management operations"""
    
    # Allowed file extensions for profile images
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        pattern = r'^09\d{8}$|^09\d{2}-\d{3}-\d{3}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_qualification(qualification):
        """Validate qualification (minimum 10 characters)"""
        return qualification and len(qualification.strip()) >= 10
    
    @staticmethod
    def allowed_file(filename):
        """Check if file has an allowed extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in InstructorController.ALLOWED_EXTENSIONS
    
    @staticmethod
    def generate_instructor_code():
        """Generate a unique instructor code"""
        year = datetime.now().year
        count = Instructor.query.count() + 1
        return f"INS-{year}-{str(count).zfill(4)}"
    
    # =============================================
    # CREATE INSTRUCTOR
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def create_instructor():
        """Create a new instructor"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = [
                'first_name', 'last_name', 'email', 'phone_number',
                'date_of_birth', 'gender', 'qualification',
                'employment_type', 'joining_date'
            ]
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate email
            if not InstructorController.validate_email(data['email']):
                return jsonify({'error': 'Invalid email format'}), 400
            
            # Check if email exists
            if Instructor.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email already exists'}), 400
            
            # Validate phone
            if not InstructorController.validate_phone(data['phone_number']):
                return jsonify({'error': 'Invalid phone number format. Use 09XXXXXXXX'}), 400
            
            # Validate date of birth
            try:
                dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                age = date.today().year - dob.year - ((date.today().month, date.today().day) < (dob.month, dob.day))
                if age < 18:
                    return jsonify({'error': 'Instructor must be at least 18 years old'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
            # Validate gender
            valid_genders = ['Male', 'Female', 'Other']
            if data['gender'] not in valid_genders:
                return jsonify({'error': 'Invalid gender'}), 400
            
            # Validate qualification
            if not InstructorController.validate_qualification(data['qualification']):
                return jsonify({'error': 'Qualification must be at least 10 characters'}), 400
            
            # Validate employment type
            valid_employment = ['Full Time', 'Part Time', 'Contract']
            if data['employment_type'] not in valid_employment:
                return jsonify({'error': 'Invalid employment type'}), 400
            
            # Validate joining date
            try:
                joining_date = datetime.strptime(data['joining_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid joining date format. Use YYYY-MM-DD'}), 400
            
            # Validate experience
            years_of_experience = data.get('years_of_experience', 0)
            if years_of_experience < 0:
                return jsonify({'error': 'Years of experience cannot be negative'}), 400
            
            # Generate instructor code
            instructor_code = InstructorController.generate_instructor_code()
            
            # Create instructor
            instructor = Instructor(
                instructor_code=instructor_code,
                first_name=data['first_name'].strip(),
                middle_name=data.get('middle_name', '').strip() if data.get('middle_name') else None,
                last_name=data['last_name'].strip(),
                date_of_birth=dob,
                gender=data['gender'],
                email=data['email'].strip().lower(),
                phone_number=data['phone_number'].strip(),
                address=data.get('address', '').strip() if data.get('address') else None,
                city=data.get('city', '').strip() if data.get('city') else None,
                qualification=data['qualification'].strip(),
                years_of_experience=years_of_experience,
                bio=data.get('bio', '').strip() if data.get('bio') else None,
                employment_type=data['employment_type'],
                joining_date=joining_date,
                department=data.get('department', '').strip() if data.get('department') else None,
                status='Active'
            )
            
            db.session.add(instructor)
            db.session.commit()
            
            # Add specializations if provided
            if data.get('specializations'):
                for spec in data['specializations']:
                    specialization = InstructorSpecialization(
                        instructor_id=instructor.instructor_id,
                        skill_name=spec.get('skill_name', '').strip(),
                        years_of_experience=spec.get('years_of_experience', 0),
                        proficiency_level=spec.get('proficiency_level', 'Advanced'),
                        is_primary_skill=spec.get('is_primary_skill', False)
                    )
                    db.session.add(specialization)
                db.session.commit()
            
            return jsonify({
                'message': 'Instructor created successfully',
                'instructor': instructor.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # READ INSTRUCTORS (List with Search, Filter, Sort, Pagination)
    # =============================================
    
    @staticmethod
    @login_required
    def list_instructors():
        """List all instructors with search, filter, sort, and pagination"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            search = request.args.get('search', '')
            status = request.args.get('status', '')
            department = request.args.get('department', '')
            employment_type = request.args.get('employment_type', '')
            sort_by = request.args.get('sort_by', 'created_at')
            sort_order = request.args.get('sort_order', 'desc')
            
            # Build query
            query = Instructor.query
            
            # Apply search filter
            if search:
                query = query.filter(
                    (Instructor.first_name.ilike(f'%{search}%')) |
                    (Instructor.last_name.ilike(f'%{search}%')) |
                    (Instructor.email.ilike(f'%{search}%')) |
                    (Instructor.instructor_code.ilike(f'%{search}%')) |
                    (Instructor.phone_number.ilike(f'%{search}%'))
                )
            
            # Apply status filter
            if status:
                query = query.filter(Instructor.status == status)
            
            # Apply department filter
            if department:
                query = query.filter(Instructor.department.ilike(f'%{department}%'))
            
            # Apply employment type filter
            if employment_type:
                query = query.filter(Instructor.employment_type == employment_type)
            
            # Apply sorting
            valid_sort_fields = ['instructor_id', 'instructor_code', 'first_name', 'last_name', 
                                 'years_of_experience', 'created_at', 'status']
            if sort_by in valid_sort_fields:
                if sort_order.lower() == 'asc':
                    query = query.order_by(getattr(Instructor, sort_by).asc())
                else:
                    query = query.order_by(getattr(Instructor, sort_by).desc())
            else:
                query = query.order_by(Instructor.created_at.desc())
            
            # Paginate
            instructors = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'data': [instructor.to_dict() for instructor in instructors.items],
                'total': instructors.total,
                'page': instructors.page,
                'per_page': instructors.per_page,
                'total_pages': instructors.pages,
                'has_prev': instructors.has_prev,
                'has_next': instructors.has_next,
                'filters': {
                    'search': search,
                    'status': status,
                    'department': department,
                    'employment_type': employment_type,
                    'sort_by': sort_by,
                    'sort_order': sort_order
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # READ SINGLE INSTRUCTOR
    # =============================================
    
    @staticmethod
    @login_required
    def get_instructor(instructor_id):
        """Get instructor details by ID"""
        try:
            instructor = Instructor.query.get(instructor_id)
            if not instructor:
                return jsonify({'error': 'Instructor not found'}), 404
            
            # Get specializations
            specializations = InstructorSpecialization.query.filter_by(
                instructor_id=instructor_id
            ).all()
            
            return jsonify({
                'instructor': instructor.to_dict(),
                'specializations': [spec.to_dict() for spec in specializations]
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # UPDATE INSTRUCTOR
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def update_instructor(instructor_id):
        """Update an existing instructor"""
        try:
            instructor = Instructor.query.get(instructor_id)
            if not instructor:
                return jsonify({'error': 'Instructor not found'}), 404
            
            data = request.get_json()
            
            # Update personal information
            if data.get('first_name'):
                instructor.first_name = data['first_name'].strip()
            
            if data.get('middle_name') is not None:
                instructor.middle_name = data['middle_name'].strip() if data['middle_name'] else None
            
            if data.get('last_name'):
                instructor.last_name = data['last_name'].strip()
            
            # Update email (with validation)
            if data.get('email'):
                if not InstructorController.validate_email(data['email']):
                    return jsonify({'error': 'Invalid email format'}), 400
                existing = Instructor.query.filter_by(email=data['email']).first()
                if existing and existing.instructor_id != instructor_id:
                    return jsonify({'error': 'Email already exists'}), 400
                instructor.email = data['email'].strip().lower()
            
            # Update phone (with validation)
            if data.get('phone_number'):
                if not InstructorController.validate_phone(data['phone_number']):
                    return jsonify({'error': 'Invalid phone number format'}), 400
                instructor.phone_number = data['phone_number'].strip()
            
            if data.get('address') is not None:
                instructor.address = data['address'].strip() if data['address'] else None
            
            if data.get('city') is not None:
                instructor.city = data['city'].strip() if data['city'] else None
            
            # Update qualification
            if data.get('qualification'):
                if not InstructorController.validate_qualification(data['qualification']):
                    return jsonify({'error': 'Qualification must be at least 10 characters'}), 400
                instructor.qualification = data['qualification'].strip()
            
            # Update experience
            if data.get('years_of_experience') is not None:
                if data['years_of_experience'] < 0:
                    return jsonify({'error': 'Years of experience cannot be negative'}), 400
                instructor.years_of_experience = data['years_of_experience']
            
            if data.get('bio') is not None:
                instructor.bio = data['bio'].strip() if data['bio'] else None
            
            # Update employment
            if data.get('employment_type'):
                valid_employment = ['Full Time', 'Part Time', 'Contract']
                if data['employment_type'] not in valid_employment:
                    return jsonify({'error': 'Invalid employment type'}), 400
                instructor.employment_type = data['employment_type']
            
            if data.get('department') is not None:
                instructor.department = data['department'].strip() if data['department'] else None
            
            # Update gender
            if data.get('gender'):
                valid_genders = ['Male', 'Female', 'Other']
                if data['gender'] not in valid_genders:
                    return jsonify({'error': 'Invalid gender'}), 400
                instructor.gender = data['gender']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Instructor updated successfully',
                'instructor': instructor.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # ADD SPECIALIZATION
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def add_specialization(instructor_id):
        """Add a specialization to an instructor"""
        try:
            instructor = Instructor.query.get(instructor_id)
            if not instructor:
                return jsonify({'error': 'Instructor not found'}), 404
            
            data = request.get_json()
            
            if not data.get('skill_name'):
                return jsonify({'error': 'Skill name is required'}), 400
            
            # Check if skill already exists for this instructor
            existing = InstructorSpecialization.query.filter_by(
                instructor_id=instructor_id,
                skill_name=data['skill_name'].strip()
            ).first()
            if existing:
                return jsonify({'error': 'Skill already exists for this instructor'}), 400
            
            specialization = InstructorSpecialization(
                instructor_id=instructor_id,
                skill_name=data['skill_name'].strip(),
                years_of_experience=data.get('years_of_experience', 0),
                proficiency_level=data.get('proficiency_level', 'Advanced'),
                skill_description=data.get('skill_description', '').strip() if data.get('skill_description') else None,
                is_primary_skill=data.get('is_primary_skill', False)
            )
            
            db.session.add(specialization)
            db.session.commit()
            
            return jsonify({
                'message': 'Specialization added successfully',
                'specialization': specialization.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # REMOVE SPECIALIZATION
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def remove_specialization(spec_id):
        """Remove a specialization"""
        try:
            specialization = InstructorSpecialization.query.get(spec_id)
            if not specialization:
                return jsonify({'error': 'Specialization not found'}), 404
            
            db.session.delete(specialization)
            db.session.commit()
            
            return jsonify({'message': 'Specialization removed successfully'}), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # UPDATE SPECIALIZATION
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def update_specialization(spec_id):
        """Update a specialization"""
        try:
            specialization = InstructorSpecialization.query.get(spec_id)
            if not specialization:
                return jsonify({'error': 'Specialization not found'}), 404
            
            data = request.get_json()
            
            if data.get('skill_name'):
                specialization.skill_name = data['skill_name'].strip()
            
            if data.get('years_of_experience') is not None:
                specialization.years_of_experience = data['years_of_experience']
            
            if data.get('proficiency_level'):
                valid_levels = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
                if data['proficiency_level'] not in valid_levels:
                    return jsonify({'error': 'Invalid proficiency level'}), 400
                specialization.proficiency_level = data['proficiency_level']
            
            if data.get('skill_description') is not None:
                specialization.skill_description = data['skill_description'].strip() if data['skill_description'] else None
            
            if data.get('is_primary_skill') is not None:
                # If setting this as primary, unset other primary skills
                if data['is_primary_skill']:
                    InstructorSpecialization.query.filter_by(
                        instructor_id=specialization.instructor_id,
                        is_primary_skill=True
                    ).update({'is_primary_skill': False})
                specialization.is_primary_skill = data['is_primary_skill']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Specialization updated successfully',
                'specialization': specialization.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # DEACTIVATE INSTRUCTOR (Soft Delete)
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def deactivate_instructor(instructor_id):
        """Soft delete an instructor (set status to Inactive)"""
        try:
            instructor = Instructor.query.get(instructor_id)
            if not instructor:
                return jsonify({'error': 'Instructor not found'}), 404
            
            if instructor.status == 'Inactive':
                return jsonify({'error': 'Instructor is already inactive'}), 400
            
            instructor.status = 'Inactive'
            db.session.commit()
            
            return jsonify({
                'message': f'Instructor {instructor.full_name} deactivated successfully',
                'instructor': instructor.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # ACTIVATE INSTRUCTOR
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def activate_instructor(instructor_id):
        """Activate an instructor"""
        try:
            instructor = Instructor.query.get(instructor_id)
            if not instructor:
                return jsonify({'error': 'Instructor not found'}), 404
            
            if instructor.status == 'Active':
                return jsonify({'error': 'Instructor is already active'}), 400
            
            instructor.status = 'Active'
            db.session.commit()
            
            return jsonify({
                'message': f'Instructor {instructor.full_name} activated successfully',
                'instructor': instructor.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # PERMANENT DELETE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin'])
    def delete_instructor(instructor_id):
        """Permanently delete an instructor"""
        try:
            instructor = Instructor.query.get(instructor_id)
            if not instructor:
                return jsonify({'error': 'Instructor not found'}), 404
            
            # Check if instructor has course assignments
            if instructor.course_assignments.count() > 0:
                return jsonify({'error': 'Cannot delete instructor with active course assignments'}), 400
            
            full_name = instructor.full_name
            db.session.delete(instructor)
            db.session.commit()
            
            return jsonify({
                'message': f'Instructor {full_name} deleted permanently'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # UPLOAD PROFILE IMAGE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def upload_profile_image(instructor_id):
        """Upload profile image for an instructor"""
        try:
            instructor = Instructor.query.get(instructor_id)
            if not instructor:
                return jsonify({'error': 'Instructor not found'}), 404
            
            # Check if user has permission
            if not (current_user.is_admin() or current_user.is_manager() or 
                    (current_user.is_instructor() and current_user.instructor_id == instructor_id)):
                return jsonify({'error': 'Permission denied'}), 403
            
            if 'image' not in request.files:
                return jsonify({'error': 'No image file provided'}), 400
            
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not InstructorController.allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif'}), 400
            
            # Save file
            filename = secure_filename(file.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            new_filename = f"instructor_{instructor_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
            
            upload_dir = os.path.join('uploads', 'instructors')
            os.makedirs(upload_dir, exist_ok=True)
            
            file_path = os.path.join(upload_dir, new_filename)
            file.save(file_path)
            
            instructor.profile_image = file_path
            db.session.commit()
            
            return jsonify({
                'message': 'Profile image uploaded successfully',
                'profile_image': file_path
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET INSTRUCTOR STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_instructor_stats():
        """Get instructor statistics"""
        try:
            total = Instructor.query.count()
            active = Instructor.query.filter_by(status='Active').count()
            inactive = Instructor.query.filter_by(status='Inactive').count()
            on_leave = Instructor.query.filter_by(status='On Leave').count()
            
            # Employment type breakdown
            employment_stats = {}
            types = ['Full Time', 'Part Time', 'Contract']
            for emp_type in types:
                employment_stats[emp_type] = Instructor.query.filter_by(employment_type=emp_type).count()
            
            # Gender breakdown
            male = Instructor.query.filter_by(gender='Male').count()
            female = Instructor.query.filter_by(gender='Female').count()
            other = Instructor.query.filter_by(gender='Other').count()
            
            # Experience breakdown
            exp_0_5 = Instructor.query.filter(Instructor.years_of_experience.between(0, 5)).count()
            exp_6_10 = Instructor.query.filter(Instructor.years_of_experience.between(6, 10)).count()
            exp_11_20 = Instructor.query.filter(Instructor.years_of_experience.between(11, 20)).count()
            exp_20_plus = Instructor.query.filter(Instructor.years_of_experience > 20).count()
            
            return jsonify({
                'total_instructors': total,
                'active_instructors': active,
                'inactive_instructors': inactive,
                'on_leave_instructors': on_leave,
                'employment_breakdown': employment_stats,
                'gender_breakdown': {
                    'male': male,
                    'female': female,
                    'other': other
                },
                'experience_breakdown': {
                    '0-5 years': exp_0_5,
                    '6-10 years': exp_6_10,
                    '11-20 years': exp_11_20,
                    '20+ years': exp_20_plus
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
