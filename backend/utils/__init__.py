from .helpers import *
from .decorators import *
from .validators import *
from .security import *

# =============================================
# EXPORT ALL FUNCTIONS AND CLASSES
# =============================================

__all__ = [
    # Helpers
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
    'paginate',
    
    # Decorators
    'role_required',
    'admin_required',
    'instructor_required',
    'trainee_required',
    'manager_required',
    
    # Validators
    'Validators',
    'validate_json',
    'validate_fields',
    'Sanitizer',
    
    # Security
    'hash_password',
    'verify_password',
    'sanitize_input',
    'log_error',
    'log_info',
    'log_warning',
    'rate_limit',
    'require_json',
    'validate_params',
    'require_login',
    'require_roles',
    'require_admin',
    'require_manager',
    'AppException',
    'handle_exception'
]

# =============================================
# MODULE INFORMATION
# =============================================

__version__ = '1.0.0'
__author__ = 'STTIMS Team'
__description__ = 'Utility functions for STTIMS backend'

# =============================================
# PRINT MODULE INFORMATION (Optional)
# =============================================

if __name__ == '__main__':
    print(f"📦 STTIMS Utils Package v{__version__}")
    print(f"   Author: {__author__}")
    print(f"   Description: {__description__}")
    print("\n📋 Available exports:")
    for item in __all__:
        print(f"   - {item}")
