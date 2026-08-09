from flask import request, jsonify
from flask_login import login_required, current_user
from models import Trainee
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime, date
import re
import os
from werkzeug.utils import secure_filename

class TraineeController:
    """Controller for trainee management operations"""
    
    # Allowed file extensions for profile images
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number (Ethiopian format)"""
        # Accepts: 09XXXXXXXX or 09XX-XXX-XXX format
        pattern = r'^09\d{8}$|^09\d{2}-\d{3}-\d{3}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_age(date_of_birth):
        """Validate age (must be at least 16 years old)"""
        if not date_of_birth:
            return False
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age >= 16
    
    @staticmethod
    def allowed_file(filename):
        """Check if file has an allowed extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in TraineeController.ALLOWED_EXTENSIONS
    
    @staticmethod
    def generate_trainee_code():
        """Generate a unique trainee code"""
        year = datetime.now().year
        count = Trainee.query.count() + 1
        return f"T-{year}-{str(count).zfill(4)}"
    
    # =============================================
    # CREATE TRAINEE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def create_trainee():
        """Create a new trainee"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = [
                'first_name', 'last_name', 'email', 'phone_number',
                'date_of_birth', 'gender', 'educational_level'
            ]
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate email
            if not TraineeController.validate_email(data['email']):
                return jsonify({'error': 'Invalid email format'}), 400
            
            # Check if email exists
            if Trainee.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email already exists'}), 400
            
            # Validate phone
            if not TraineeController.validate_phone(data['phone_number']):
                return jsonify({'error': 'Invalid phone number format. Use 09XXXXXXXX'}), 400
            
            # Validate date of birth
            try:
                dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                if not TraineeController.validate_age(dob):
                    return jsonify({'error': 'Trainee must be at least 16 years old'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
            # Validate gender
            valid_genders = ['Male', 'Female', 'Other']
            if data['gender'] not in valid_genders:
                return jsonify({'error': 'Invalid gender'}), 400
            
            # Validate educational level
            valid_levels = ['High School', 'Diploma', 'BSc', 'MSc', 'PhD', 'Other']
            if data['educational_level'] not in valid_levels:
                return jsonify({'error': 'Invalid educational level'}), 400
            
            # Generate trainee code
            trainee_code = TraineeController.generate_trainee_code()
            
            # Create trainee
            trainee = Trainee(
                trainee_code=trainee_code,
                first_name=data['first_name'].strip(),
                middle_name=data.get('middle_name', '').strip() if data.get('middle_name') else None,
                last_name=data['last_name'].strip(),
                date_of_birth=dob,
                gender=data['gender'],
                email=data['email'].strip().lower(),
                phone_number=data['phone_number'].strip(),
                alternative_phone=data.get('alternative_phone', '').strip() if data.get('alternative_phone') else None,
                address=data.get('address', '').strip() if data.get('address') else None,
                city=data.get('city', '').strip() if data.get('city') else None,
                state_region=data.get('state_region', '').strip() if data.get('state_region') else None,
                country=data.get('country', 'Ethiopia').strip(),
                educational_level=data['educational_level'],
                occupation=data.get('occupation', '').strip() if data.get('occupation') else None,
                organization=data.get('organization', '').strip() if data.get('organization') else None,
                emergency_contact_name=data.get('emergency_contact_name', '').strip() if data.get('emergency_contact_name') else None,
                emergency_contact_phone=data.get('emergency_contact_phone', '').strip() if data.get('emergency_contact_phone') else None,
                status='Active'
            )
            
            db.session.add(trainee)
            db.session.commit()
            
            return jsonify({
                'message': 'Trainee created successfully',
                'trainee': trainee.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # READ TRAINEES (List with Search, Filter, Sort, Pagination)
    # =============================================
    
    @staticmethod
    @login_required
    def list_trainees():
        """List all trainees with search, filter, sort, and pagination"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            search = request.args.get('search', '')
            gender = request.args.get('gender', '')
            educational_level = request.args.get('educational_level', '')
            status = request.args.get('status', '')
            sort_by = request.args.get('sort_by', 'created_at')
            sort_order = request.args.get('sort_order', 'desc')
            
            # Build query
            query = Trainee.query
            
            # Apply search filter
            if search:
                query = query.filter(
                    (Trainee.first_name.ilike(f'%{search}%')) |
                    (Trainee.last_name.ilike(f'%{search}%')) |
                    (Trainee.email.ilike(f'%{search}%')) |
                    (Trainee.trainee_code.ilike(f'%{search}%')) |
                    (Trainee.phone_number.ilike(f'%{search}%'))
                )
            
            # Apply gender filter
            if gender:
                query = query.filter(Trainee.gender == gender)
            
            # Apply educational level filter
            if educational_level:
                query = query.filter(Trainee.educational_level == educational_level)
            
            # Apply status filter
            if status:
                query = query.filter(Trainee.status == status)
            
            # Apply sorting
            valid_sort_fields = ['trainee_id', 'trainee_code', 'first_name', 'last_name', 'email', 'created_at', 'status']
            if sort_by in valid_sort_fields:
                if sort_order.lower() == 'asc':
                    query = query.order_by(getattr(Trainee, sort_by).asc())
                else:
                    query = query.order_by(getattr(Trainee, sort_by).desc())
            else:
                query = query.order_by(Trainee.created_at.desc())
            
            # Paginate
            trainees = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'data': [trainee.to_dict() for trainee in trainees.items],
                'total': trainees.total,
                'page': trainees.page,
                'per_page': trainees.per_page,
                'total_pages': trainees.pages,
                'has_prev': trainees.has_prev,
                'has_next': trainees.has_next,
                'filters': {
                    'search': search,
                    'gender': gender,
                    'educational_level': educational_level,
                    'status': status,
                    'sort_by': sort_by,
                    'sort_order': sort_order
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # READ SINGLE TRAINEE
    # =============================================
    
    @staticmethod
    @login_required
    def get_trainee(trainee_id):
        """Get trainee details by ID"""
        try:
            trainee = Trainee.query.get(trainee_id)
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 404
            
            return jsonify({'trainee': trainee.to_dict()}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # UPDATE TRAINEE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def update_trainee(trainee_id):
        """Update an existing trainee"""
        try:
            trainee = Trainee.query.get(trainee_id)
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 404
            
            data = request.get_json()
            
            # Update fields
            if data.get('first_name'):
                trainee.first_name = data['first_name'].strip()
            
            if data.get('middle_name') is not None:
                trainee.middle_name = data['middle_name'].strip() if data['middle_name'] else None
            
            if data.get('last_name'):
                trainee.last_name = data['last_name'].strip()
            
            # Update email (with validation)
            if data.get('email'):
                if not TraineeController.validate_email(data['email']):
                    return jsonify({'error': 'Invalid email format'}), 400
                existing = Trainee.query.filter_by(email=data['email']).first()
                if existing and existing.trainee_id != trainee_id:
                    return jsonify({'error': 'Email already exists'}), 400
                trainee.email = data['email'].strip().lower()
            
            # Update phone (with validation)
            if data.get('phone_number'):
                if not TraineeController.validate_phone(data['phone_number']):
                    return jsonify({'error': 'Invalid phone number format. Use 09XXXXXXXX'}), 400
                trainee.phone_number = data['phone_number'].strip()
            
            if data.get('alternative_phone') is not None:
                trainee.alternative_phone = data['alternative_phone'].strip() if data['alternative_phone'] else None
            
            if data.get('address') is not None:
                trainee.address = data['address'].strip() if data['address'] else None
            
            if data.get('city'):
                trainee.city = data['city'].strip()
            
            if data.get('state_region'):
                trainee.state_region = data['state_region'].strip()
            
            if data.get('country'):
                trainee.country = data['country'].strip()
            
            # Update educational level
            if data.get('educational_level'):
                valid_levels = ['High School', 'Diploma', 'BSc', 'MSc', 'PhD', 'Other']
                if data['educational_level'] not in valid_levels:
                    return jsonify({'error': 'Invalid educational level'}), 400
                trainee.educational_level = data['educational_level']
            
            if data.get('occupation') is not None:
                trainee.occupation = data['occupation'].strip() if data['occupation'] else None
            
            if data.get('organization') is not None:
                trainee.organization = data['organization'].strip() if data['organization'] else None
            
            # Update emergency contact
            if data.get('emergency_contact_name') is not None:
                trainee.emergency_contact_name = data['emergency_contact_name'].strip() if data['emergency_contact_name'] else None
            
            if data.get('emergency_contact_phone') is not None:
                trainee.emergency_contact_phone = data['emergency_contact_phone'].strip() if data['emergency_contact_phone'] else None
            
            # Update gender
            if data.get('gender'):
                valid_genders = ['Male', 'Female', 'Other']
                if data['gender'] not in valid_genders:
                    return jsonify({'error': 'Invalid gender'}), 400
                trainee.gender = data['gender']
            
            db.session.commit()
            
            return jsonify({
                'message': 'Trainee updated successfully',
                'trainee': trainee.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # SOFT DELETE (Deactivate)
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def deactivate_trainee(trainee_id):
        """Soft delete a trainee (set status to Inactive)"""
        try:
            trainee = Trainee.query.get(trainee_id)
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 404
            
            if trainee.status == 'Inactive':
                return jsonify({'error': 'Trainee is already inactive'}), 400
            
            trainee.status = 'Inactive'
            db.session.commit()
            
            return jsonify({
                'message': f'Trainee {trainee.full_name} deactivated successfully',
                'trainee': trainee.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # ACTIVATE TRAINEE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def activate_trainee(trainee_id):
        """Activate a trainee (set status to Active)"""
        try:
            trainee = Trainee.query.get(trainee_id)
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 404
            
            if trainee.status == 'Active':
                return jsonify({'error': 'Trainee is already active'}), 400
            
            trainee.status = 'Active'
            db.session.commit()
            
            return jsonify({
                'message': f'Trainee {trainee.full_name} activated successfully',
                'trainee': trainee.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # PERMANENT DELETE (Hard Delete)
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin'])
    def delete_trainee(trainee_id):
        """Permanently delete a trainee (use with caution)"""
        try:
            trainee = Trainee.query.get(trainee_id)
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 404
            
            # Check if trainee has enrollments
            if trainee.enrollments.count() > 0:
                return jsonify({'error': 'Cannot delete trainee with existing enrollments'}), 400
            
            full_name = trainee.full_name
            db.session.delete(trainee)
            db.session.commit()
            
            return jsonify({
                'message': f'Trainee {full_name} deleted permanently'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # UPLOAD PROFILE IMAGE
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Trainee'])
    def upload_profile_image(trainee_id):
        """Upload profile image for a trainee"""
        try:
            trainee = Trainee.query.get(trainee_id)
            if not trainee:
                return jsonify({'error': 'Trainee not found'}), 404
            
            # Check if user has permission
            if not (current_user.is_admin() or current_user.is_manager() or 
                    (current_user.is_trainee() and current_user.trainee_id == trainee_id)):
                return jsonify({'error': 'Permission denied'}), 403
            
            if 'image' not in request.files:
                return jsonify({'error': 'No image file provided'}), 400
            
            file = request.files['image']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not TraineeController.allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif'}), 400
            
            # Secure filename and save
            filename = secure_filename(file.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            new_filename = f"trainee_{trainee_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
            
            # Ensure upload directory exists
            upload_dir = os.path.join('uploads', 'trainees')
            os.makedirs(upload_dir, exist_ok=True)
            
            file_path = os.path.join(upload_dir, new_filename)
            file.save(file_path)
            
            # Update trainee profile image
            trainee.profile_image = file_path
            db.session.commit()
            
            return jsonify({
                'message': 'Profile image uploaded successfully',
                'profile_image': file_path
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # GET TRAINEE STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_trainee_stats():
        """Get trainee statistics"""
        try:
            total = Trainee.query.count()
            active = Trainee.query.filter_by(status='Active').count()
            inactive = Trainee.query.filter_by(status='Inactive').count()
            suspended = Trainee.query.filter_by(status='Suspended').count()
            
            # Gender breakdown
            male = Trainee.query.filter_by(gender='Male').count()
            female = Trainee.query.filter_by(gender='Female').count()
            other = Trainee.query.filter_by(gender='Other').count()
            
            # Educational level breakdown
            education_stats = {}
            levels = ['High School', 'Diploma', 'BSc', 'MSc', 'PhD', 'Other']
            for level in levels:
                education_stats[level] = Trainee.query.filter_by(educational_level=level).count()
            
            return jsonify({
                'total_trainees': total,
                'active_trainees': active,
                'inactive_trainees': inactive,
                'suspended_trainees': suspended,
                'gender_breakdown': {
                    'male': male,
                    'female': female,
                    'other': other
                },
                'education_breakdown': education_stats
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # BULK IMPORT TRAINEES
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def bulk_import_trainees():
        """Bulk import trainees from JSON array"""
        try:
            data = request.get_json()
            if not data or not isinstance(data, list):
                return jsonify({'error': 'Expected array of trainees'}), 400
            
            created = []
            errors = []
            
            for idx, trainee_data in enumerate(data):
                try:
                    # Validate required fields
                    required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'gender', 'educational_level']
                    for field in required_fields:
                        if not trainee_data.get(field):
                            errors.append({'index': idx, 'error': f'{field} is required'})
                            continue
                    
                    # Validate email
                    if not TraineeController.validate_email(trainee_data['email']):
                        errors.append({'index': idx, 'error': 'Invalid email format'})
                        continue
                    
                    if Trainee.query.filter_by(email=trainee_data['email']).first():
                        errors.append({'index': idx, 'error': 'Email already exists'})
                        continue
                    
                    # Validate phone
                    if not TraineeController.validate_phone(trainee_data['phone_number']):
                        errors.append({'index': idx, 'error': 'Invalid phone number format'})
                        continue
                    
                    # Validate date of birth
                    try:
                        dob = datetime.strptime(trainee_data['date_of_birth'], '%Y-%m-%d').date()
                        if not TraineeController.validate_age(dob):
                            errors.append({'index': idx, 'error': 'Trainee must be at least 16 years old'})
                            continue
                    except ValueError:
                        errors.append({'index': idx, 'error': 'Invalid date format. Use YYYY-MM-DD'})
                        continue
                    
                    # Validate gender
                    if trainee_data['gender'] not in ['Male', 'Female', 'Other']:
                        errors.append({'index': idx, 'error': 'Invalid gender'})
                        continue
                    
                    # Create trainee
                    trainee_code = TraineeController.generate_trainee_code()
                    trainee = Trainee(
                        trainee_code=trainee_code,
                        first_name=trainee_data['first_name'].strip(),
                        middle_name=trainee_data.get('middle_name', '').strip() if trainee_data.get('middle_name') else None,
                        last_name=trainee_data['last_name'].strip(),
                        date_of_birth=dob,
                        gender=trainee_data['gender'],
                        email=trainee_data['email'].strip().lower(),
                        phone_number=trainee_data['phone_number'].strip(),
                        alternative_phone=trainee_data.get('alternative_phone', '').strip() if trainee_data.get('alternative_phone') else None,
                        address=trainee_data.get('address', '').strip() if trainee_data.get('address') else None,
                        city=trainee_data.get('city', '').strip() if trainee_data.get('city') else None,
                        state_region=trainee_data.get('state_region', '').strip() if trainee_data.get('state_region') else None,
                        country=trainee_data.get('country', 'Ethiopia').strip(),
                        educational_level=trainee_data['educational_level'],
                        occupation=trainee_data.get('occupation', '').strip() if trainee_data.get('occupation') else None,
                        organization=trainee_data.get('organization', '').strip() if trainee_data.get('organization') else None,
                        emergency_contact_name=trainee_data.get('emergency_contact_name', '').strip() if trainee_data.get('emergency_contact_name') else None,
                        emergency_contact_phone=trainee_data.get('emergency_contact_phone', '').strip() if trainee_data.get('emergency_contact_phone') else None,
                        status='Active'
                    )
                    
                    db.session.add(trainee)
                    created.append(trainee_code)
                    
                except Exception as e:
                    errors.append({'index': idx, 'error': str(e)})
            
            if created:
                db.session.commit()
            
            return jsonify({
                'message': f'Created {len(created)} trainees',
                'created': created,
                'errors': errors,
                'total_processed': len(data),
                'success_count': len(created),
                'error_count': len(errors)
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
