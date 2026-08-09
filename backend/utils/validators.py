import re
from datetime import datetime, date
from flask import request, jsonify
from functools import wraps

class Validators:
    """Collection of validation utilities"""
    
    @staticmethod
    def validate_required(data, required_fields):
        """
        Validate that all required fields are present and not empty
        
        Args:
            data (dict): Data to validate
            required_fields (list): List of required field names
        
        Returns:
            tuple: (is_valid, error_message)
        """
        for field in required_fields:
            if not data.get(field):
                return False, f"'{field}' is required"
            if isinstance(data[field], str) and not data[field].strip():
                return False, f"'{field}' cannot be empty"
        return True, None
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number"""
        if not phone:
            return True
        pattern = r'^09\d{8}$|^09\d{2}-\d{3}-\d{3}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_username(username):
        """Validate username"""
        if not username:
            return False
        pattern = r'^[a-zA-Z0-9_]{3,20}$'
        return re.match(pattern, username) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if not password:
            return False, "Password is required"
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        return True, "Password is valid"
    
    @staticmethod
    def validate_date(date_str, format='%Y-%m-%d'):
        """Validate date format"""
        if not date_str:
            return True, None
        try:
            parsed = datetime.strptime(date_str, format).date()
            return True, parsed
        except ValueError:
            return False, f"Invalid date format. Use {format}"
    
    @staticmethod
    def validate_age(date_of_birth, min_age=16):
        """Validate age"""
        if not date_of_birth:
            return False, "Date of birth is required"
        today = date.today()
        age = today.year - date_of_birth.year - (
            (today.month, today.day) < (date_of_birth.month, date_of_birth.day)
        )
        if age < min_age:
            return False, f"Must be at least {min_age} years old"
        return True, None
    
    @staticmethod
    def validate_in_range(value, min_val, max_val, field_name):
        """Validate value is within range"""
        if value is None:
            return True, None
        if value < min_val:
            return False, f"{field_name} must be at least {min_val}"
        if value > max_val:
            return False, f"{field_name} must not exceed {max_val}"
        return True, None
    
    @staticmethod
    def validate_unique(model, field, value, exclude_id=None):
        """Validate that a field value is unique"""
        if not value:
            return True, None
        query = model.query.filter(getattr(model, field) == value)
        if exclude_id:
            query = query.filter(getattr(model, 'id') != exclude_id)
        if query.first():
            return False, f"{field} already exists"
        return True, None
    
    @staticmethod
    def validate_enum(value, valid_values, field_name):
        """Validate that value is in enum list"""
        if not value:
            return True, None
        if value not in valid_values:
            return False, f"Invalid {field_name}. Must be one of: {', '.join(valid_values)}"
        return True, None

class Sanitizer:
    """Data sanitization utilities"""
    
    @staticmethod
    def sanitize_string(value):
        """Sanitize a string"""
        if not value:
            return None
        value = value.strip()
        value = re.sub(r'<[^>]*>', '', value)
        return value
    
    @staticmethod
    def sanitize_email(email):
        """Sanitize email"""
        if not email:
            return None
        return email.strip().lower()
    
    @staticmethod
    def sanitize_phone(phone):
        """Sanitize phone number"""
        if not phone:
            return None
        return re.sub(r'[^0-9]', '', phone)

def validate_json(f):
    """Decorator to validate JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        if not request.get_json():
            return jsonify({'error': 'Invalid JSON payload'}), 400
        return f(*args, **kwargs)
    return decorated_function

def validate_fields(required_fields=None, optional_fields=None):
    """
    Decorator to validate required and optional fields
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            
            if required_fields:
                for field in required_fields:
                    if not data.get(field):
                        return jsonify({'error': f"'{field}' is required"}), 400
                    if isinstance(data[field], str) and not data[field].strip():
                        return jsonify({'error': f"'{field}' cannot be empty"}), 400
            
            if optional_fields:
                for field, validator in optional_fields.items():
                    if field in data and data[field] is not None:
                        if isinstance(data[field], str) and not data[field].strip():
                            continue
                        if callable(validator):
                            is_valid, error = validator(data[field])
                            if not is_valid:
                                return jsonify({'error': error}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
