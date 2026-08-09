from flask import Blueprint, request, jsonify, session
from models import User
from models import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username (alphanumeric, 3-20 chars)"""
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

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
    return True, 'Password is valid'

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    POST /api/auth/register
    Body: {username, email, password, role, trainee_id?, instructor_id?}
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password', 'role']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate role
    valid_roles = ['Admin', 'Instructor', 'Trainee', 'Manager']
    if data['role'] not in valid_roles:
        return jsonify({'error': 'Invalid role. Must be: Admin, Instructor, Trainee, or Manager'}), 400
    
    # Validate username
    if not validate_username(data['username']):
        return jsonify({'error': 'Username must be 3-20 characters (letters, numbers, underscores)'}), 400
    
    # Validate email
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate password
    is_valid, message = validate_password(data['password'])
    if not is_valid:
        return jsonify({'error': message}), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        role=data['role']
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
        'message': 'User registered successfully',
        'user': {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'status': user.status
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    POST /api/auth/login
    Body: {username_or_email, password}
    """
    data = request.get_json()
    
    if not data.get('username_or_email') or not data.get('password'):
        return jsonify({'error': 'Username/email and password are required'}), 400
    
    # Try to find user by username or email
    user = User.query.filter(
        (User.username == data['username_or_email']) | 
        (User.email == data['username_or_email'])
    ).first()
    
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Check if account is locked
    if user.is_locked():
        return jsonify({'error': 'Account is locked. Please contact administrator.'}), 403
    
    # Check password
    if not user.check_password(data['password']):
        user.increment_login_attempts()
        db.session.commit()
        remaining_attempts = 5 - user.login_attempts
        return jsonify({
            'error': 'Invalid username or password',
            'remaining_attempts': remaining_attempts
        }), 401
    
    # Check if account is active
    if not user.is_active():
        return jsonify({'error': 'Account is inactive. Please contact administrator.'}), 403
    
    # Login successful
    user.reset_login_attempts()
    user.update_last_login()
    db.session.commit()
    
    login_user(user, remember=True)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Logout user
    POST /api/auth/logout
    """
    username = current_user.username
    logout_user()
    return jsonify({'message': f'User {username} logged out successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """
    Get current authenticated user
    GET /api/auth/me
    """
    return jsonify({
        'user': current_user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """
    Update user profile
    PUT /api/auth/profile
    Body: {username?, email?, password?}
    """
    data = request.get_json()
    user = current_user
    
    # Update username
    if data.get('username') and data['username'] != user.username:
        if not validate_username(data['username']):
            return jsonify({'error': 'Username must be 3-20 characters (letters, numbers, underscores)'}), 400
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        user.username = data['username']
    
    # Update email
    if data.get('email') and data['email'] != user.email:
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        user.email = data['email']
    
    # Update password
    if data.get('password'):
        is_valid, message = validate_password(data['password'])
        if not is_valid:
            return jsonify({'error': message}), 400
        user.set_password(data['password'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    """
    Check if user is authenticated
    GET /api/auth/check-auth
    """
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        }), 200
    else:
        return jsonify({
            'authenticated': False
        }), 200
