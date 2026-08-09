from flask import Blueprint
from flask_login import login_required
from controllers.batch_controller import BatchController
from utils.decorators import require_module

batch_bp = Blueprint('batch', __name__, url_prefix='/api/batches')

@batch_bp.route('/', methods=['GET'])
@login_required
@require_module('batches')
def list_batches():
    """List all batches with search, filter, sort, and pagination"""
    return BatchController.list_batches()

@batch_bp.route('/stats', methods=['GET'])
@login_required
@require_module('batches')
def get_batch_stats():
    """Get batch statistics"""
    return BatchController.get_batch_stats()

@batch_bp.route('/<int:batch_id>', methods=['GET'])
@login_required
@require_module('batches')
def get_batch(batch_id):
    """Get batch details by ID"""
    return BatchController.get_batch(batch_id)

@batch_bp.route('/', methods=['POST'])
@login_required
@require_module('batches')
def create_batch():
    """Create a new batch"""
    return BatchController.create_batch()

@batch_bp.route('/<int:batch_id>', methods=['PUT'])
@login_required
@require_module('batches')
def update_batch(batch_id):
    """Update an existing batch"""
    return BatchController.update_batch(batch_id)

@batch_bp.route('/<int:batch_id>/close', methods=['POST'])
@login_required
@require_module('batches')
def close_batch(batch_id):
    """Close a batch (mark as Completed)"""
    return BatchController.close_batch(batch_id)

@batch_bp.route('/<int:batch_id>/cancel', methods=['POST'])
@login_required
@require_module('batches')
def cancel_batch(batch_id):
    """Cancel a batch"""
    return BatchController.cancel_batch(batch_id)

@batch_bp.route('/<int:batch_id>/start', methods=['POST'])
@login_required
@require_module('batches')
def start_batch(batch_id):
    """Start a batch (mark as Ongoing)"""
    return BatchController.start_batch(batch_id)
