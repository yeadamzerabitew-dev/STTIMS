/* ============================================
   STTIMS - Validation Helper Functions
   ============================================ */

/**
 * Show validation error for a field
 */
function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    field.classList.add('is-invalid');
    field.classList.remove('is-valid');
    
    const feedback = field.nextElementSibling;
    if (feedback && feedback.classList.contains('invalid-feedback')) {
        feedback.textContent = message;
    }
}

/**
 * Show validation success for a field
 */
function showFieldSuccess(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    field.classList.remove('is-invalid');
    field.classList.add('is-valid');
}

/**
 * Clear validation for a field
 */
function clearFieldValidation(fieldId) {
    const field = document.getElementById(fieldId);
    if (!field) return;
    
    field.classList.remove('is-invalid', 'is-valid');
    const feedback = field.nextElementSibling;
    if (feedback && feedback.classList.contains('invalid-feedback')) {
        feedback.textContent = '';
    }
}

/**
 * Validate email on input
 */
function validateEmailInput(input) {
    const value = input.value.trim();
    if (!value) {
        showFieldError(input.id, 'Email is required');
        return false;
    }
    if (!Validator.email(value)) {
        showFieldError(input.id, 'Please enter a valid email address');
        return false;
    }
    showFieldSuccess(input.id);
    return true;
}

/**
 * Validate phone on input
 */
function validatePhoneInput(input) {
    const value = input.value.trim();
    if (!value) {
        showFieldError(input.id, 'Phone number is required');
        return false;
    }
    if (!Validator.phone(value)) {
        showFieldError(input.id, 'Please enter a valid phone number (e.g., 0912345678)');
        return false;
    }
    showFieldSuccess(input.id);
    return true;
}

/**
 * Validate password on input
 */
function validatePasswordInput(input) {
    const value = input.value;
    if (!value) {
        showFieldError(input.id, 'Password is required');
        return false;
    }
    if (!Validator.password(value)) {
        showFieldError(input.id, 'Password must be 8+ chars with uppercase, lowercase, number, and special character');
        return false;
    }
    showFieldSuccess(input.id);
    return true;
}

/**
 * Validate password match
 */
function validatePasswordMatch(passwordId, confirmId) {
    const password = document.getElementById(passwordId).value;
    const confirm = document.getElementById(confirmId).value;
    
    if (!confirm) {
        showFieldError(confirmId, 'Please confirm your password');
        return false;
    }
    if (password !== confirm) {
        showFieldError(confirmId, 'Passwords do not match');
        return false;
    }
    showFieldSuccess(confirmId);
    return true;
}

/**
 * Validate numeric input
 */
function validateNumericInput(input, min = null, max = null) {
    const value = parseFloat(input.value);
    if (isNaN(value) || value < 0) {
        showFieldError(input.id, 'Please enter a valid positive number');
        return false;
    }
    if (min !== null && value < min) {
        showFieldError(input.id, `Value must be at least ${min}`);
        return false;
    }
    if (max !== null && value > max) {
        showFieldError(input.id, `Value must not exceed ${max}`);
        return false;
    }
    showFieldSuccess(input.id);
    return true;
}

/**
 * Validate date input
 */
function validateDateInput(input, allowPast = true, allowFuture = true) {
    const value = input.value;
    if (!value) {
        showFieldError(input.id, 'Date is required');
        return false;
    }
    if (!Validator.date(value)) {
        showFieldError(input.id, 'Please enter a valid date (YYYY-MM-DD)');
        return false;
    }
    const date = new Date(value);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (!allowPast && date < today) {
        showFieldError(input.id, 'Date cannot be in the past');
        return false;
    }
    if (!allowFuture && date > today) {
        showFieldError(input.id, 'Date cannot be in the future');
        return false;
    }
    showFieldSuccess(input.id);
    return true;
}

/**
 * Check if form is valid
 */
function isFormValid(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const inputs = form.querySelectorAll('.is-invalid');
    return inputs.length === 0;
}

/**
 * Get form data as object
 */
function getFormData(formId) {
    const form = document.getElementById(formId);
    if (!form) return {};
    
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    return data;
}
