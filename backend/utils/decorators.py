from functools import wraps
from flask import jsonify, request
from flask_login import current_user

# =============================================
# ROLE-BASED DECORATORS
# =============================================

def role_required(roles):
    """
    Decorator to require specific roles
    Usage: @role_required(['Admin', 'Manager'])
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'Authentication required'}), 401
            
            if current_user.role not in roles:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'required_roles': roles,
                    'user_role': current_user.role
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorator to require Admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        
        if current_user.role != 'Admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def instructor_required(f):
    """Decorator to require Instructor, Manager, or Admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        
        if current_user.role not in ['Admin', 'Manager', 'Instructor']:
            return jsonify({'error': 'Instructor access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def trainee_required(f):
    """Decorator to require Trainee role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        
        if current_user.role not in ['Admin', 'Trainee']:
            return jsonify({'error': 'Trainee access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    """Decorator to require Manager or Admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        
        if current_user.role not in ['Admin', 'Manager']:
            return jsonify({'error': 'Manager access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def require_module(module_name):
    """
    Restrict a route to roles that have access to `module_name`,
    per User.can_access_module(). Use it BELOW @login_required:

        @some_bp.route('/', methods=['GET'])
        @login_required
        @require_module('trainees')
        def list_trainees():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'Unauthorized'}), 401
            if not current_user.can_access_module(module_name):
                return jsonify({
                    'error': f"Forbidden: role '{current_user.role}' cannot access this resource"
                }), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator

# =============================================
# REQUEST VALIDATION DECORATORS
# =============================================

def require_json(f):
    """Decorator to require JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        if not request.get_json():
            return jsonify({'error': 'Invalid JSON payload'}), 400
        return f(*args, **kwargs)
    return decorated_function

def require_login(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# =============================================
# EXPORT ALL DECORATORS
# =============================================

__all__ = [
    'role_required',
    'admin_required',
    'instructor_required',
    'trainee_required',
    'manager_required',
    'require_module',
    'require_json',
    'require_login'
]
