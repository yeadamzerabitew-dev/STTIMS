import os
import logging
from functools import wraps
from flask import request, jsonify, current_app
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

# =============================================
# PASSWORD UTILITIES
# =============================================

def hash_password(password):
    """Hash a password using Werkzeug"""
    return generate_password_hash(password)

def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return check_password_hash(password_hash, password)

# =============================================
# INPUT SANITIZATION
# =============================================

def sanitize_input(value):
    """Sanitize user input to prevent XSS and injection"""
    if value is None:
        return None
    if isinstance(value, str):
        value = re.sub(r'<script.*?>.*?</script>', '', value, flags=re.IGNORECASE | re.DOTALL)
        value = re.sub(r'on\w+="[^"]*"', '', value, flags=re.IGNORECASE)
        value = re.sub(r"on\w+='[^']*'", '', value, flags=re.IGNORECASE)
        value = re.sub(r'[<>]', '', value)
        return value.strip()
    return value

# =============================================
# LOGGING
# =============================================

def log_error(message, error=None, data=None):
    """Log an error with context"""
    logger = logging.getLogger(__name__)
    log_message = f"ERROR: {message}"
    if error:
        log_message += f" | Error: {str(error)}"
    if data:
        log_message += f" | Data: {data}"
    logger.error(log_message)

def log_info(message, data=None):
    """Log an info message"""
    logger = logging.getLogger(__name__)
    log_message = f"INFO: {message}"
    if data:
        log_message += f" | Data: {data}"
    logger.info(log_message)

def log_warning(message, data=None):
    """Log a warning message"""
    logger = logging.getLogger(__name__)
    log_message = f"WARNING: {message}"
    if data:
        log_message += f" | Data: {data}"
    logger.warning(log_message)

# =============================================
# RATE LIMITING
# =============================================

_rate_limit_store = {}

def rate_limit(limit=60, window=60):
    """
    Rate limit decorator
    
    Args:
        limit (int): Max requests per window
        window (int): Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            import time
            ip = request.remote_addr
            current_time = int(time.time())
            
            if ip not in _rate_limit_store:
                _rate_limit_store[ip] = []
            
            _rate_limit_store[ip] = [
                t for t in _rate_limit_store[ip] 
                if current_time - t < window
            ]
            
            if len(_rate_limit_store[ip]) >= limit:
                return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
            
            _rate_limit_store[ip].append(current_time)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# =============================================
# REQUEST VALIDATION DECORATORS
# =============================================

def require_json(f):
    """Decorator to require JSON content type"""
    from flask import request
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        if not request.get_json():
            return jsonify({'error': 'Invalid JSON payload'}), 400
        return f(*args, **kwargs)
    return decorated_function

def validate_params(required_params=None, optional_params=None):
    """
    Decorator to validate request parameters
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or {}
            
            if required_params:
                missing = []
                for param in required_params:
                    if param not in data or data[param] is None:
                        missing.append(param)
                if missing:
                    return jsonify({
                        'error': f'Missing required parameters: {", ".join(missing)}'
                    }), 400
            
            if optional_params:
                for param, param_type in optional_params.items():
                    if param in data and data[param] is not None:
                        if not isinstance(data[param], param_type):
                            return jsonify({
                                'error': f'Parameter "{param}" must be of type {param_type.__name__}'
                            }), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# =============================================
# PERMISSION DECORATORS
# =============================================

def require_login(f):
    """Decorator to require login"""
    from flask_login import current_user
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def require_roles(allowed_roles):
    """
    Decorator to require specific roles
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': 'Authentication required'}), 401
            if current_user.role not in allowed_roles:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'required_roles': allowed_roles,
                    'user_role': current_user.role
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_admin(f):
    """Decorator to require Admin role"""
    return require_roles(['Admin'])

def require_manager(f):
    """Decorator to require Manager role"""
    return require_roles(['Admin', 'Manager'])

# =============================================
# ERROR HANDLING
# =============================================

class AppException(Exception):
    """Custom application exception"""
    def __init__(self, message, status_code=400, details=None):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)

def handle_exception(e):
    """Global exception handler"""
    if isinstance(e, AppException):
        response = {
            'error': e.message,
            'status_code': e.status_code
        }
        if e.details:
            response['details'] = e.details
        return jsonify(response), e.status_code
    
    log_error(f"Unexpected error: {str(e)}")
    
    return jsonify({
        'error': 'An unexpected error occurred',
        'message': str(e) if current_app.config.get('DEBUG') else 'Internal server error'
    }), 500
