from flask import Blueprint, request, jsonify
from flask_login import login_required
from controllers.user_controller import UserController
from utils.decorators import require_module

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@login_required
@require_module('users')
def list_users():
    """List all users"""
    return UserController.list_users()

@user_bp.route('/stats', methods=['GET'])
@login_required
@require_module('users')
def get_user_stats():
    """Get user statistics"""
    return UserController.get_user_stats()

@user_bp.route('/<int:user_id>', methods=['GET'])
@login_required
@require_module('users')
def get_user(user_id):
    """Get user details by ID"""
    return UserController.get_user(user_id)

@user_bp.route('/', methods=['POST'])
@login_required
@require_module('users')
def create_user():
    """Create a new user"""
    return UserController.create_user()

@user_bp.route('/<int:user_id>', methods=['PUT'])
@login_required
@require_module('users')
def update_user(user_id):
    """Update an existing user"""
    return UserController.update_user(user_id)

@user_bp.route('/<int:user_id>/deactivate', methods=['POST'])
@login_required
@require_module('users')
def deactivate_user(user_id):
    """Deactivate a user"""
    return UserController.deactivate_user(user_id)

@user_bp.route('/<int:user_id>/activate', methods=['POST'])
@login_required
@require_module('users')
def activate_user(user_id):
    """Activate a user"""
    return UserController.activate_user(user_id)

@user_bp.route('/<int:user_id>/reset-password', methods=['POST'])
@login_required
@require_module('users')
def reset_password(user_id):
    """Reset user password"""
    return UserController.reset_password(user_id)

@user_bp.route('/<int:user_id>/unlock', methods=['POST'])
@login_required
@require_module('users')
def unlock_account(user_id):
    """Unlock a locked account"""
    return UserController.unlock_account(user_id)

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@login_required
@require_module('users')
def delete_user(user_id):
    """Delete a user"""
    return UserController.delete_user(user_id)
