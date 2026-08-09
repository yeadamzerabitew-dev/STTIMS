from flask import Blueprint
from flask_login import login_required
from controllers.assessment_controller import AssessmentController
from utils.decorators import require_module

assessment_bp = Blueprint('assessment', __name__, url_prefix='/api/assessments')

@assessment_bp.route('/', methods=['GET'])
@login_required
@require_module('assessments')
def list_assessments():
    """List all assessments with filters"""
    return AssessmentController.list_assessments()

@assessment_bp.route('/stats', methods=['GET'])
@login_required
@require_module('assessments')
def get_assessment_stats():
    """Get assessment statistics"""
    return AssessmentController.get_assessment_stats()

@assessment_bp.route('/<int:assessment_id>', methods=['GET'])
@login_required
@require_module('assessments')
def get_assessment(assessment_id):
    """Get assessment details by ID"""
    return AssessmentController.get_assessment(assessment_id)

@assessment_bp.route('/', methods=['POST'])
@login_required
@require_module('assessments')
def create_assessment():
    """Create a new assessment"""
    return AssessmentController.create_assessment()

@assessment_bp.route('/<int:assessment_id>', methods=['PUT'])
@login_required
@require_module('assessments')
def update_assessment(assessment_id):
    """Update an existing assessment"""
    return AssessmentController.update_assessment(assessment_id)

@assessment_bp.route('/<int:assessment_id>/cancel', methods=['POST'])
@login_required
@require_module('assessments')
def cancel_assessment(assessment_id):
    """Cancel an assessment"""
    return AssessmentController.cancel_assessment(assessment_id)

@assessment_bp.route('/<int:assessment_id>/complete', methods=['POST'])
@login_required
@require_module('assessments')
def complete_assessment(assessment_id):
    """Complete an assessment"""
    return AssessmentController.complete_assessment(assessment_id)
