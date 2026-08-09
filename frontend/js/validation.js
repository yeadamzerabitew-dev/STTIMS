/* ============================================
   STTIMS - Front-End Validation
   ============================================ */

/**
 * Validation Rules and Patterns
 */
const VALIDATION = {
    // Email pattern
    EMAIL: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    
    // Ethiopian Phone: 09XXXXXXXX or 09XX-XXX-XXX
    PHONE_ETH: /^09\d{8}$|^09\d{2}-\d{3}-\d{3}$/,
    
    // General phone: Allows international format
    PHONE_GENERAL: /^\+?[\d\s-]{10,15}$/,
    
    // Username: 3-20 alphanumeric characters
    USERNAME: /^[a-zA-Z0-9_]{3,20}$/,
    
    // Password: At least 8 characters with requirements
    PASSWORD_MIN_LENGTH: 8,
    
    // Date format: YYYY-MM-DD
    DATE: /^\d{4}-\d{2}-\d{2}$/,
    
    // Course code: Alphanumeric, 3-10 chars
    COURSE_CODE: /^[A-Z0-9]{3,10}$/,
    
    // Trainee code: T-YYYY-XXXX
    TRAINEE_CODE: /^T-\d{4}-\d{4}$/,
    
    // Names: Letters, spaces, hyphens
    NAME: /^[a-zA-Z\s\-']{2,50}$/,
    
    // Numeric: Positive numbers
    NUMERIC_POSITIVE: /^\d+(\.\d+)?$/,
    
    // Decimal with 2 places
    DECIMAL_2: /^\d+(\.\d{1,2})?$/
};

/**
 * Validation Messages
 */
const MESSAGES = {
    required: 'This field is required',
    email: 'Please enter a valid email address',
    emailExists: 'This email is already registered',
    phone: 'Please enter a valid phone number (e.g., 0912345678)',
    username: 'Username must be 3-20 characters (letters, numbers, underscores)',
    usernameExists: 'This username is already taken',
    password: 'Password must be at least 8 characters',
    passwordMatch: 'Passwords do not match',
    passwordStrength: 'Password must contain uppercase, lowercase, number, and special character',
    date: 'Please enter a valid date (YYYY-MM-DD)',
    datePast: 'Date cannot be in the past',
    dateFuture: 'Date cannot be in the future',
    numeric: 'Please enter a valid number',
    numericPositive: 'Please enter a positive number',
    numericRange: 'Value must be between {min} and {max}',
    minLength: 'Minimum {length} characters required',
    maxLength: 'Maximum {length} characters allowed',
    select: 'Please select an option',
    code: 'Please enter a valid code (alphanumeric, 3-10 characters)',
    confirm: 'Please confirm your selection',
    age: 'Age must be at least {age} years',
    capacity: 'Capacity must be greater than 0',
    fee: 'Fee must be a positive amount',
    marks: 'Marks must be between 0 and {max}',
    weightage: 'Total weightage cannot exceed 100%',
    duplicate: 'This value already exists'
};

/**
 * Validator Class
 */
class Validator {
    
    // ============================================
    // REQUIRED FIELDS
    // ============================================
    static required(value) {
        if (value === null || value === undefined) return false;
        if (typeof value === 'string') return value.trim().length > 0;
        if (Array.isArray(value)) return value.length > 0;
        return true;
    }
    
    // ============================================
    // EMAIL VALIDATION
    // ============================================
    static email(value) {
        if (!value) return true; // Allow empty (use required for required)
        return VALIDATION.EMAIL.test(value);
    }
    
    // ============================================
    // PHONE VALIDATION
    // ============================================
    static phone(value, type = 'ethiopian') {
        if (!value) return true;
        const pattern = type === 'ethiopian' ? VALIDATION.PHONE_ETH : VALIDATION.PHONE_GENERAL;
        return pattern.test(value);
    }
    
    // ============================================
    // USERNAME VALIDATION
    // ============================================
    static username(value) {
        if (!value) return false;
        return VALIDATION.USERNAME.test(value);
    }
    
    // ============================================
    // PASSWORD VALIDATION
    // ============================================
    static password(value) {
        if (!value) return false;
        if (value.length < VALIDATION.PASSWORD_MIN_LENGTH) return false;
        
        // Check for at least one uppercase, lowercase, number, special character
        const hasUpper = /[A-Z]/.test(value);
        const hasLower = /[a-z]/.test(value);
        const hasNumber = /[0-9]/.test(value);
        const hasSpecial = /[^A-Za-z0-9]/.test(value);
        
        return hasUpper && hasLower && hasNumber && hasSpecial;
    }
    
    static passwordStrength(value) {
        if (!value) return 0;
        
        let strength = 0;
        if (value.length >= 8) strength++;
        if (value.length >= 12) strength++;
        if (/[A-Z]/.test(value)) strength++;
        if (/[a-z]/.test(value)) strength++;
        if (/[0-9]/.test(value)) strength++;
        if (/[^A-Za-z0-9]/.test(value)) strength++;
        
        return strength;
    }
    
    static getPasswordStrengthLabel(strength) {
        if (strength >= 5) return { label: 'Very Strong', class: 'very-strong' };
        if (strength >= 4) return { label: 'Strong', class: 'strong' };
        if (strength >= 3) return { label: 'Medium', class: 'medium' };
        if (strength >= 2) return { label: 'Weak', class: 'weak' };
        return { label: 'Very Weak', class: 'very-weak' };
    }
    
    // ============================================
    // PASSWORD MATCH
    // ============================================
    static passwordMatch(password, confirm) {
        return password === confirm;
    }
    
    // ============================================
    // DATE VALIDATION
    // ============================================
    static date(value) {
        if (!value) return true;
        if (!VALIDATION.DATE.test(value)) return false;
        
        const date = new Date(value);
        return !isNaN(date.getTime());
    }
    
    static dateInPast(value) {
        if (!value) return true;
        const date = new Date(value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        return date < today;
    }
    
    static dateInFuture(value) {
        if (!value) return true;
        const date = new Date(value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        return date > today;
    }
    
    static dateRange(start, end) {
        if (!start || !end) return true;
        return new Date(start) <= new Date(end);
    }
    
    static age(value, minAge = 16) {
        if (!value) return true;
        const birthDate = new Date(value);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const m = today.getMonth() - birthDate.getMonth();
        if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        return age >= minAge;
    }
    
    // ============================================
    // NUMERIC VALIDATION
    // ============================================
    static numeric(value) {
        if (value === null || value === undefined || value === '') return true;
        return !isNaN(parseFloat(value)) && isFinite(value);
    }
    
    static numericPositive(value) {
        if (!Validator.numeric(value)) return false;
        return parseFloat(value) > 0;
    }
    
    static numericNonNegative(value) {
        if (!Validator.numeric(value)) return false;
        return parseFloat(value) >= 0;
    }
    
    static numericRange(value, min, max) {
        if (!Validator.numeric(value)) return false;
        const num = parseFloat(value);
        return num >= min && num <= max;
    }
    
    static integer(value) {
        if (!Validator.numeric(value)) return false;
        return Number.isInteger(parseFloat(value));
    }
    
    // ============================================
    // LENGTH VALIDATION
    // ============================================
    static minLength(value, min) {
        if (!value) return false;
        return value.length >= min;
    }
    
    static maxLength(value, max) {
        if (!value) return true;
        return value.length <= max;
    }
    
    static betweenLength(value, min, max) {
        if (!value) return false;
        return value.length >= min && value.length <= max;
    }
    
    // ============================================
    // NAME VALIDATION
    // ============================================
    static name(value) {
        if (!value) return false;
        return VALIDATION.NAME.test(value);
    }
    
    // ============================================
    // COURSE CODE
    // ============================================
    static courseCode(value) {
        if (!value) return false;
        return VALIDATION.COURSE_CODE.test(value);
    }
    
    // ============================================
    // TRAINEE CODE
    // ============================================
    static traineeCode(value) {
        if (!value) return true;
        return VALIDATION.TRAINEE_CODE.test(value);
    }
    
    // ============================================
    // WEIGHTAGE TOTAL (for assessments)
    // ============================================
    static weightageTotal(assessments, currentId = null) {
        let total = 0;
        assessments.forEach(a => {
            if (a.id !== currentId) {
                total += a.weightage || 0;
            }
        });
        return total;
    }
    
    static validateWeightage(weightage, currentTotal, maxTotal = 100) {
        return currentTotal + weightage <= maxTotal;
    }
    
    // ============================================
    // FORM VALIDATION HELPERS
    // ============================================
    static validateForm(formId) {
        const form = document.getElementById(formId);
        if (!form) return { valid: false, errors: ['Form not found'] };
        
        const inputs = form.querySelectorAll('[data-validate]');
        let isValid = true;
        let errors = [];
        
        inputs.forEach(input => {
            const rules = input.dataset.validate.split(' ');
            const value = input.value;
            let fieldValid = true;
            
            rules.forEach(rule => {
                const [ruleName, ...params] = rule.split(':');
                const result = Validator.validateRule(value, ruleName, params);
                if (!result.valid) {
                    fieldValid = false;
                    errors.push({
                        field: input.name || input.id,
                        message: result.message
                    });
                }
            });
            
            if (!fieldValid) {
                input.classList.add('is-invalid');
                isValid = false;
            } else {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
            }
        });
        
        return { valid: isValid, errors };
    }
    
    static validateRule(value, rule, params) {
        switch(rule) {
            case 'required':
                return { valid: Validator.required(value), message: MESSAGES.required };
            case 'email':
                return { valid: Validator.email(value), message: MESSAGES.email };
            case 'phone':
                return { valid: Validator.phone(value), message: MESSAGES.phone };
            case 'username':
                return { valid: Validator.username(value), message: MESSAGES.username };
            case 'password':
                return { valid: Validator.password(value), message: MESSAGES.password };
            case 'min':
                const min = parseInt(params[0]);
                return { valid: Validator.minLength(value, min), message: MESSAGES.minLength.replace('{length}', min) };
            case 'max':
                const max = parseInt(params[0]);
                return { valid: Validator.maxLength(value, max), message: MESSAGES.maxLength.replace('{length}', max) };
            case 'numeric':
                return { valid: Validator.numeric(value), message: MESSAGES.numeric };
            case 'numericPositive':
                return { valid: Validator.numericPositive(value), message: MESSAGES.numericPositive };
            case 'date':
                return { valid: Validator.date(value), message: MESSAGES.date };
            case 'datePast':
                return { valid: Validator.dateInPast(value), message: MESSAGES.datePast };
            case 'dateFuture':
                return { valid: Validator.dateInFuture(value), message: MESSAGES.dateFuture };
            case 'name':
                return { valid: Validator.name(value), message: 'Please enter a valid name' };
            case 'courseCode':
                return { valid: Validator.courseCode(value), message: 'Please enter a valid course code' };
            default:
                return { valid: true, message: '' };
        }
    }
}

// ============================================
// REAL-TIME VALIDATION
// ============================================
class RealTimeValidator {
    constructor() {
        this.init();
    }
    
    init() {
        // Add validation to all form inputs with data-validate attribute
        document.querySelectorAll('[data-validate]').forEach(input => {
            // Validate on blur
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
            
            // Validate on input (for real-time feedback)
            input.addEventListener('input', () => {
                if (input.classList.contains('is-invalid') || input.classList.contains('is-valid')) {
                    this.validateField(input);
                }
            });
        });
        
        // Form submission validation
        document.querySelectorAll('form[data-validate-form]').forEach(form => {
            form.addEventListener('submit', (e) => {
                const result = this.validateForm(form);
                if (!result.valid) {
                    e.preventDefault();
                    this.showErrors(result.errors);
                }
            });
        });
    }
    
    validateField(input) {
        const rules = input.dataset.validate.split(' ');
        let isValid = true;
        let errorMessage = '';
        
        rules.forEach(rule => {
            const [ruleName, ...params] = rule.split(':');
            const result = Validator.validateRule(input.value, ruleName, params);
            if (!result.valid) {
                isValid = false;
                errorMessage = result.message;
            }
        });
        
        if (!isValid) {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            if (input.nextElementSibling?.classList.contains('invalid-feedback')) {
                input.nextElementSibling.textContent = errorMessage;
            }
        } else if (input.value) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            if (input.nextElementSibling?.classList.contains('invalid-feedback')) {
                input.nextElementSibling.textContent = '';
            }
        } else {
            input.classList.remove('is-invalid', 'is-valid');
        }
        
        return { valid: isValid, message: errorMessage };
    }
    
    validateForm(form) {
        const inputs = form.querySelectorAll('[data-validate]');
        let isValid = true;
        const errors = [];
        
        inputs.forEach(input => {
            const result = this.validateField(input);
            if (!result.valid) {
                isValid = false;
                errors.push({
                    field: input.name || input.id,
                    message: result.message
                });
            }
        });
        
        return { valid: isValid, errors };
    }
    
    showErrors(errors) {
        // Show first error as alert
        if (errors.length > 0) {
            const firstError = errors[0];
            const alertContainer = document.getElementById('alertContainer');
            if (alertContainer) {
                alertContainer.innerHTML = `
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        <i class="fas fa-exclamation-circle me-2"></i>
                        ${firstError.message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                `;
            }
        }
    }
}

// ============================================
// Initialize Validators
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    window.validator = Validator;
    window.realTimeValidator = new RealTimeValidator();
});

// ============================================
// Export for use in other files
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Validator, RealTimeValidator };
}
