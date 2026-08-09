from flask import Blueprint
from flask_login import login_required
from controllers.session_controller import SessionController
from utils.decorators import require_module

session_bp = Blueprint('session', __name__, url_prefix='/api/sessions')

@session_bp.route('/', methods=['GET'])
@login_required
@require_module('sessions')
def list_sessions():
    """List all sessions with filters"""
    return SessionController.list_sessions()

@session_bp.route('/<int:session_id>', methods=['GET'])
@login_required
@require_module('sessions')
def get_session(session_id):
    """Get session details by ID"""
    return SessionController.get_session(session_id)

@session_bp.route('/', methods=['POST'])
@login_required
@require_module('sessions')
def create_session():
    """Create a new session"""
    return SessionController.create_session()

@session_bp.route('/<int:session_id>', methods=['PUT'])
@login_required
@require_module('sessions')
def update_session(session_id):
    """Update an existing session"""
    return SessionController.update_session(session_id)

@session_bp.route('/<int:session_id>/cancel', methods=['POST'])
@login_required
@require_module('sessions')
def cancel_session(session_id):
    """Cancel a session"""
    return SessionController.cancel_session(session_id)

@session_bp.route('/<int:session_id>/complete', methods=['POST'])
@login_required
@require_module('sessions')
def complete_session(session_id):
    """Complete a session"""
    return SessionController.complete_session(session_id)
