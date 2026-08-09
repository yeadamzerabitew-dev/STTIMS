from flask import request, jsonify
from flask_login import login_required, current_user
from models import User
from models import db
from utils.decorators import admin_required, role_required
from datetime import datetime
import re

class UserController:
    """Controller for user management operations"""
    
    @staticmethod
    def validate_username(username):
        """Validate username (alphanumeric, 3-20 chars)"""
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return re.match(pattern, username) is not None
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, 'Password must be at least 8 characters long'
        if not re.search(r'[A-Z]', password):
            return False, 'Password must contain at least one uppercase letter'
        if not re.search(r'[a-z]', password):
            return False, 'Password must contain at least one lowercase letter'
        if not re.search(r'[0-9]', password):
            return False, 'Password must contain at least one number'
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, 'Password must contain at least one special character'
        return True, 'Password is valid'
    
    @staticmethod
    def validate_role(role):
        """Validate role"""
        valid_roles = ['Admin', 'Manager', 'Instructor', 'Trainee']
        return role in valid_roles
    
    @staticmethod
    @login_required
    @admin_required
    def list_users():
        """List all users with pagination and filtering"""
        try:
            # Get query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            search = request.args.get('search', '')
            role_filter = request.args.get('role', '')
            status_filter = request.args.get('status', '')
            
            # Build query
            query = User.query
            
            # Apply filters
            if search:
                query = query.filter(
                    (User.username.ilike(f'%{search}%')) |
                    (User.email.ilike(f'%{search}%'))
                )
            
            if role_filter:
                query = query.filter(User.role == role_filter)
            
            if status_filter:
                query = query.filter(User.status == status_filter)
            
            # Order by creation date
            query = query.order_by(User.created_at.desc())
            
            # Paginate
            users = query.paginate(page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'data': [user.to_dict_minimal() for user in users.items],
                'total': users.total,
                'page': users.page,
                'per_page': users.per_page,
                'total_pages': users.pages,
                'has_prev': users.has_prev,
                'has_next': users.has_next
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def get_user(user_id):
        """Get user details by ID"""
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({'user': user.to_dict()}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def create_user():
        """Create a new user"""
        try:
            data = request.get_json()
            
            # Validate required fields
            required_fields = ['username', 'email', 'password', 'role']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'error': f'{field} is required'}), 400
            
            # Validate username
            if not UserController.validate_username(data['username']):
                return jsonify({'error': 'Username must be 3-20 characters (letters, numbers, underscores)'}), 400
            
            # Validate email
            if not UserController.validate_email(data['email']):
                return jsonify({'error': 'Invalid email format'}), 400
            
            # Validate password
            is_valid, message = UserController.validate_password(data['password'])
            if not is_valid:
                return jsonify({'error': message}), 400
            
            # Validate role
            if not UserController.validate_role(data['role']):
                return jsonify({'error': 'Invalid role. Must be: Admin, Manager, Instructor, or Trainee'}), 400
            
            # Check if user exists
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'error': 'Username already exists'}), 400
            
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email already exists'}), 400
            
            # Create user
            user = User(
                username=data['username'],
                email=data['email'],
                role=data['role'],
                status=data.get('status', 'Active')
            )
            user.set_password(data['password'])
            
            # Set trainee_id or instructor_id if provided
            if data.get('trainee_id'):
                user.trainee_id = data['trainee_id']
            if data.get('instructor_id'):
                user.instructor_id = data['instructor_id']
            
            db.session.add(user)
            db.session.commit()
            
            return jsonify({
                'message': 'User created successfully',
                'user': user.to_dict()
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def update_user(user_id):
        """Update an existing user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            data = request.get_json()
            
            # Update username
            if data.get('username') and data['username'] != user.username:
                if not UserController.validate_username(data['username']):
                    return jsonify({'error': 'Username must be 3-20 characters (letters, numbers, underscores)'}), 400
                if User.query.filter_by(username=data['username']).first():
                    return jsonify({'error': 'Username already exists'}), 400
                user.username = data['username']
            
            # Update email
            if data.get('email') and data['email'] != user.email:
                if not UserController.validate_email(data['email']):
                    return jsonify({'error': 'Invalid email format'}), 400
                if User.query.filter_by(email=data['email']).first():
                    return jsonify({'error': 'Email already exists'}), 400
                user.email = data['email']
            
            # Update role (only Admin can change roles)
            if data.get('role') and data['role'] != user.role:
                if not current_user.is_admin():
                    return jsonify({'error': 'Only admins can change roles'}), 403
                if not UserController.validate_role(data['role']):
                    return jsonify({'error': 'Invalid role'}), 400
                user.role = data['role']
            
            # Update status
            if data.get('status') and data['status'] != user.status:
                valid_statuses = ['Active', 'Inactive', 'Locked']
                if data['status'] not in valid_statuses:
                    return jsonify({'error': 'Invalid status'}), 400
                user.status = data['status']
            
            db.session.commit()
            
            return jsonify({
                'message': 'User updated successfully',
                'user': user.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def deactivate_user(user_id):
        """Deactivate a user (soft delete)"""
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Prevent self-deactivation
            if user.user_id == current_user.user_id:
                return jsonify({'error': 'Cannot deactivate your own account'}), 400
            
            user.status = 'Inactive'
            db.session.commit()
            
            return jsonify({
                'message': f'User {user.username} deactivated successfully',
                'user': user.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def activate_user(user_id):
        """Activate a user"""
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            user.status = 'Active'
            user.login_attempts = 0
            db.session.commit()
            
            return jsonify({
                'message': f'User {user.username} activated successfully',
                'user': user.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def reset_password(user_id):
        """Reset user password"""
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            data = request.get_json()
            
            if not data.get('new_password'):
                return jsonify({'error': 'New password is required'}), 400
            
            # Validate password
            is_valid, message = UserController.validate_password(data['new_password'])
            if not is_valid:
                return jsonify({'error': message}), 400
            
            user.set_password(data['new_password'])
            user.login_attempts = 0
            user.status = 'Active' if user.status == 'Locked' else user.status
            db.session.commit()
            
            return jsonify({
                'message': f'Password reset successfully for {user.username}',
                'user': user.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def unlock_account(user_id):
        """Unlock a locked user account"""
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if user.status != 'Locked':
                return jsonify({'error': 'Account is not locked'}), 400
            
            user.status = 'Active'
            user.login_attempts = 0
            db.session.commit()
            
            return jsonify({
                'message': f'Account {user.username} unlocked successfully',
                'user': user.to_dict_minimal()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def delete_user(user_id):
        """Delete a user (hard delete)"""
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Prevent self-deletion
            if user.user_id == current_user.user_id:
                return jsonify({'error': 'Cannot delete your own account'}), 400
            
            username = user.username
            db.session.delete(user)
            db.session.commit()
            
            return jsonify({
                'message': f'User {username} deleted successfully'
            }), 200
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @staticmethod
    @login_required
    @admin_required
    def get_user_stats():
        """Get user statistics"""
        try:
            total_users = User.query.count()
            active_users = User.query.filter_by(status='Active').count()
            inactive_users = User.query.filter_by(status='Inactive').count()
            locked_users = User.query.filter_by(status='Locked').count()
            
            # Role breakdown
            role_stats = {}
            roles = ['Admin', 'Manager', 'Instructor', 'Trainee']
            for role in roles:
                role_stats[role] = User.query.filter_by(role=role).count()
            
            return jsonify({
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': inactive_users,
                'locked_users': locked_users,
                'role_breakdown': role_stats
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
