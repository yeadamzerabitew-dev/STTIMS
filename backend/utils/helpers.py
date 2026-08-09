import os
import re
from datetime import datetime
from werkzeug.utils import secure_filename

# =============================================
# VALIDATION HELPERS
# =============================================

def validate_email(email):
    """Validate email format"""
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number (Ethiopian format)"""
    if not phone:
        return True
    pattern = r'^09\d{8}$|^09\d{2}-\d{3}-\d{3}$'
    return re.match(pattern, phone) is not None

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

def validate_username(username):
    """Validate username (alphanumeric, 3-20 chars)"""
    if not username:
        return False
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

# =============================================
# FILE HELPERS
# =============================================

def allowed_file(filename, allowed_extensions=None):
    """Check if file has an allowed extension"""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_extension(filename):
    """Get file extension"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def generate_unique_filename(filename):
    """Generate a unique filename"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    secure_name = secure_filename(filename)
    name, ext = os.path.splitext(secure_name)
    return f"{name}_{timestamp}{ext}"

# =============================================
# DATE AND TIME HELPERS
# =============================================

def format_date(date_obj, format='%Y-%m-%d'):
    """Format date object to string"""
    if date_obj is None:
        return None
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime(format)

def format_datetime(datetime_obj, format='%Y-%m-%d %H:%M:%S'):
    """Format datetime object to string"""
    if datetime_obj is None:
        return None
    if isinstance(datetime_obj, str):
        return datetime_obj
    return datetime_obj.strftime(format)

def calculate_age(birth_date):
    """Calculate age from date of birth"""
    if birth_date is None:
        return None
    today = datetime.now().date()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

# =============================================
# DICTIONARY HELPERS
# =============================================

def to_dict(obj, exclude_fields=None):
    """Convert SQLAlchemy model to dictionary"""
    if exclude_fields is None:
        exclude_fields = []
    
    if hasattr(obj, '__table__'):
        result = {}
        for column in obj.__table__.columns:
            if column.name not in exclude_fields:
                value = getattr(obj, column.name)
                if isinstance(value, datetime):
                    result[column.name] = format_datetime(value)
                else:
                    result[column.name] = value
        return result
    return obj

def paginate(query, page, per_page):
    """Paginate a query"""
    return query.paginate(page=page, per_page=per_page, error_out=False)

# =============================================
# EXPORT ALL FUNCTIONS
# =============================================

__all__ = [
    'validate_email',
    'validate_phone',
    'validate_password',
    'validate_username',
    'allowed_file',
    'get_file_extension',
    'generate_unique_filename',
    'format_date',
    'format_datetime',
    'calculate_age',
    'to_dict',
    'paginate'
]
