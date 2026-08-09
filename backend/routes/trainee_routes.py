from flask import Blueprint, request, jsonify
from flask_login import login_required
from controllers.trainee_controller import TraineeController
from utils.decorators import require_module

trainee_bp = Blueprint('trainee', __name__, url_prefix='/api/trainees')

@trainee_bp.route('/', methods=['GET'])
@login_required
@require_module('trainees')
def list_trainees():
    """List all trainees with search, filter, sort, and pagination"""
    return TraineeController.list_trainees()

@trainee_bp.route('/stats', methods=['GET'])
@login_required
@require_module('trainees')
def get_trainee_stats():
    """Get trainee statistics"""
    return TraineeController.get_trainee_stats()

@trainee_bp.route('/<int:trainee_id>', methods=['GET'])
@login_required
@require_module('trainees')
def get_trainee(trainee_id):
    """Get trainee details by ID"""
    return TraineeController.get_trainee(trainee_id)

@trainee_bp.route('/', methods=['POST'])
@login_required
@require_module('trainees')
def create_trainee():
    """Create a new trainee"""
    return TraineeController.create_trainee()

@trainee_bp.route('/bulk', methods=['POST'])
@login_required
@require_module('trainees')
def bulk_import_trainees():
    """Bulk import trainees"""
    return TraineeController.bulk_import_trainees()

@trainee_bp.route('/<int:trainee_id>', methods=['PUT'])
@login_required
@require_module('trainees')
def update_trainee(trainee_id):
    """Update an existing trainee"""
    return TraineeController.update_trainee(trainee_id)

@trainee_bp.route('/<int:trainee_id>/deactivate', methods=['POST'])
@login_required
@require_module('trainees')
def deactivate_trainee(trainee_id):
    """Deactivate a trainee (soft delete)"""
    return TraineeController.deactivate_trainee(trainee_id)

@trainee_bp.route('/<int:trainee_id>/activate', methods=['POST'])
@login_required
@require_module('trainees')
def activate_trainee(trainee_id):
    """Activate a trainee"""
    return TraineeController.activate_trainee(trainee_id)

@trainee_bp.route('/<int:trainee_id>/upload-image', methods=['POST'])
@login_required
@require_module('trainees')
def upload_profile_image(trainee_id):
    """Upload profile image for a trainee"""
    return TraineeController.upload_profile_image(trainee_id)

@trainee_bp.route('/<int:trainee_id>', methods=['DELETE'])
@login_required
@require_module('trainees')
def delete_trainee(trainee_id):
    """Permanently delete a trainee"""
    return TraineeController.delete_trainee(trainee_id)
