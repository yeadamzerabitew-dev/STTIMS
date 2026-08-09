from flask import Blueprint
from flask_login import login_required
from controllers.course_controller import CourseController
from utils.decorators import require_module

course_bp = Blueprint('course', __name__, url_prefix='/api/courses')

@course_bp.route('/', methods=['GET'])
@login_required
@require_module('courses')
def list_courses():
    """List all courses with search, filter, sort, and pagination"""
    return CourseController.list_courses()

@course_bp.route('/stats', methods=['GET'])
@login_required
@require_module('courses')
def get_course_stats():
    """Get course statistics"""
    return CourseController.get_course_stats()

@course_bp.route('/category/<int:category_id>', methods=['GET'])
@login_required
@require_module('courses')
def get_courses_by_category(category_id):
    """Get all courses in a category"""
    return CourseController.get_courses_by_category(category_id)

@course_bp.route('/<int:course_id>', methods=['GET'])
@login_required
@require_module('courses')
def get_course(course_id):
    """Get course details by ID"""
    return CourseController.get_course(course_id)

@course_bp.route('/', methods=['POST'])
@login_required
@require_module('courses')
def create_course():
    """Create a new course"""
    return CourseController.create_course()

@course_bp.route('/<int:course_id>', methods=['PUT'])
@login_required
@require_module('courses')
def update_course(course_id):
    """Update an existing course"""
    return CourseController.update_course(course_id)

@course_bp.route('/<int:course_id>/archive', methods=['POST'])
@login_required
@require_module('courses')
def archive_course(course_id):
    """Archive a course"""
    return CourseController.archive_course(course_id)

@course_bp.route('/<int:course_id>/activate', methods=['POST'])
@login_required
@require_module('courses')
def activate_course(course_id):
    """Activate a course"""
    return CourseController.activate_course(course_id)

@course_bp.route('/<int:course_id>', methods=['DELETE'])
@login_required
@require_module('courses')
def delete_course(course_id):
    """Permanently delete a course"""
    return CourseController.delete_course(course_id)
