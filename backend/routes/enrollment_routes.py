from flask import Blueprint
from flask_login import login_required
from controllers.enrollment_controller import EnrollmentController
from utils.decorators import require_module

enrollment_bp = Blueprint('enrollment', __name__, url_prefix='/api/enrollments')

@enrollment_bp.route('/', methods=['GET'])
@login_required
@require_module('enrollments')
def list_enrollments():
    """List all enrollments with search, filter, sort, and pagination"""
    return EnrollmentController.list_enrollments()

@enrollment_bp.route('/stats', methods=['GET'])
@login_required
@require_module('enrollments')
def get_enrollment_stats():
    """Get enrollment statistics"""
    return EnrollmentController.get_enrollment_stats()

@enrollment_bp.route('/<int:enrollment_id>', methods=['GET'])
@login_required
@require_module('enrollments')
def get_enrollment(enrollment_id):
    """Get enrollment details by ID"""
    return EnrollmentController.get_enrollment(enrollment_id)

@enrollment_bp.route('/', methods=['POST'])
@login_required
@require_module('enrollments')
def create_enrollment():
    """Create a new enrollment"""
    return EnrollmentController.create_enrollment()

@enrollment_bp.route('/<int:enrollment_id>', methods=['PUT'])
@login_required
@require_module('enrollments')
def update_enrollment(enrollment_id):
    """Update an existing enrollment"""
    return EnrollmentController.update_enrollment(enrollment_id)

@enrollment_bp.route('/<int:enrollment_id>/drop', methods=['POST'])
@login_required
@require_module('enrollments')
def drop_enrollment(enrollment_id):
    """Drop an enrollment"""
    return EnrollmentController.drop_enrollment(enrollment_id)

@enrollment_bp.route('/<int:enrollment_id>/complete', methods=['POST'])
@login_required
@require_module('enrollments')
def complete_enrollment(enrollment_id):
    """Complete an enrollment"""
    return EnrollmentController.complete_enrollment(enrollment_id)

@enrollment_bp.route('/<int:enrollment_id>/payment', methods=['POST'])
@login_required
@require_module('enrollments')
def process_payment(enrollment_id):
    """Process a payment for an enrollment"""
    return EnrollmentController.process_payment(enrollment_id)
