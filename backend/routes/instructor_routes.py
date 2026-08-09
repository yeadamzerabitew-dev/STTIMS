from flask import Blueprint, request, jsonify
from flask_login import login_required
from controllers.instructor_controller import InstructorController
from models import Instructor, db
from sqlalchemy import or_
from utils.decorators import require_module

instructor_bp = Blueprint('instructor', __name__, url_prefix='/api/instructors')

@instructor_bp.route('/', methods=['GET'])
@login_required
@require_module('instructors')
def list_instructors():
    """List all instructors with search, filter, sort, and pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        department = request.args.get('department', '')
        status = request.args.get('status', '')
        
        query = Instructor.query
        
        # Apply search filter
        if search:
            query = query.filter(
                or_(
                    Instructor.first_name.like(f'%{search}%'),
                    Instructor.last_name.like(f'%{search}%'),
                    Instructor.email.like(f'%{search}%'),
                    Instructor.instructor_code.like(f'%{search}%')
                )
            )
        
        # Apply department filter
        if department:
            query = query.filter(Instructor.department == department)
        
        # Apply status filter
        if status:
            query = query.filter(Instructor.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        instructors = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Calculate total pages
        total_pages = (total + per_page - 1) // per_page if total > 0 else 1
        
        return jsonify({
            'success': True,
            'data': [i.to_dict() for i in instructors],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@instructor_bp.route('/stats', methods=['GET'])
@login_required
@require_module('instructors')
def get_instructor_stats():
    """Get instructor statistics"""
    return InstructorController.get_instructor_stats()

@instructor_bp.route('/<int:instructor_id>', methods=['GET'])
@login_required
@require_module('instructors')
def get_instructor(instructor_id):
    """Get instructor details by ID"""
    return InstructorController.get_instructor(instructor_id)

@instructor_bp.route('/', methods=['POST'])
@login_required
@require_module('instructors')
def create_instructor():
    """Create a new instructor"""
    return InstructorController.create_instructor()

@instructor_bp.route('/<int:instructor_id>', methods=['PUT'])
@login_required
@require_module('instructors')
def update_instructor(instructor_id):
    """Update an existing instructor"""
    return InstructorController.update_instructor(instructor_id)

@instructor_bp.route('/<int:instructor_id>/specializations', methods=['POST'])
@login_required
@require_module('instructors')
def add_specialization(instructor_id):
    """Add a specialization to an instructor"""
    return InstructorController.add_specialization(instructor_id)

@instructor_bp.route('/specializations/<int:spec_id>', methods=['PUT'])
@login_required
@require_module('instructors')
def update_specialization(spec_id):
    """Update a specialization"""
    return InstructorController.update_specialization(spec_id)

@instructor_bp.route('/specializations/<int:spec_id>', methods=['DELETE'])
@login_required
@require_module('instructors')
def remove_specialization(spec_id):
    """Remove a specialization"""
    return InstructorController.remove_specialization(spec_id)

@instructor_bp.route('/<int:instructor_id>/deactivate', methods=['POST'])
@login_required
@require_module('instructors')
def deactivate_instructor(instructor_id):
    """Deactivate an instructor (soft delete)"""
    return InstructorController.deactivate_instructor(instructor_id)

@instructor_bp.route('/<int:instructor_id>/activate', methods=['POST'])
@login_required
@require_module('instructors')
def activate_instructor(instructor_id):
    """Activate an instructor"""
    return InstructorController.activate_instructor(instructor_id)

@instructor_bp.route('/<int:instructor_id>/upload-image', methods=['POST'])
@login_required
@require_module('instructors')
def upload_profile_image(instructor_id):
    """Upload profile image for an instructor"""
    return InstructorController.upload_profile_image(instructor_id)

@instructor_bp.route('/<int:instructor_id>', methods=['DELETE'])
@login_required
@require_module('instructors')
def delete_instructor(instructor_id):
    """Permanently delete an instructor"""
    return InstructorController.delete_instructor(instructor_id)
