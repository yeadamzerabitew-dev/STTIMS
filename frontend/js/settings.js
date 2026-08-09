/* ============================================
   STTIMS - Settings JavaScript
   ============================================ */

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadSettings();
});

// ============================================
// Setup Event Listeners
// ============================================
function setupEventListeners() {
    // Institution Form
    document.getElementById('institutionForm').addEventListener('submit', function(e) {
        e.preventDefault();
        saveInstitutionSettings();
    });
    
    // Email Settings Form
    document.getElementById('emailSettingsForm').addEventListener('submit', function(e) {
        e.preventDefault();
        saveEmailSettings();
    });
    
    // Password Form
    document.getElementById('passwordForm').addEventListener('submit', function(e) {
        e.preventDefault();
        changePassword();
    });
    
    // Logo Upload
    document.getElementById('logoInput').addEventListener('change', function(e) {
        handleLogoUpload(e);
    });
    
    // Certificate Template
    document.getElementById('certificateTemplate').addEventListener('change', function() {
        updateTemplatePreview();
    });
}

// ============================================
// Load Settings
// ============================================
function loadSettings() {
    // Load saved settings from localStorage
    const settings = JSON.parse(localStorage.getItem('sttims_settings') || '{}');
    
    if (settings.institutionName) {
        document.getElementById('institutionName').value = settings.institutionName;
    }
    if (settings.institutionCode) {
        document.getElementById('institutionCode').value = settings.institutionCode;
    }
    if (settings.institutionAddress) {
        document.getElementById('institutionAddress').value = settings.institutionAddress;
    }
    if (settings.institutionPhone) {
        document.getElementById('institutionPhone').value = settings.institutionPhone;
    }
    if (settings.institutionEmail) {
        document.getElementById('institutionEmail').value = settings.institutionEmail;
    }
    if (settings.theme) {
        selectTheme(settings.theme);
    }
    if (settings.certificateTemplate) {
        document.getElementById('certificateTemplate').value = settings.certificateTemplate;
    }
    if (settings.logo) {
        document.getElementById('logoImage').src = settings.logo;
    }
}

// ============================================
// Save Institution Settings
// ============================================
function saveInstitutionSettings() {
    const settings = {
        institutionName: document.getElementById('institutionName').value,
        institutionCode: document.getElementById('institutionCode').value,
        institutionAddress: document.getElementById('institutionAddress').value,
        institutionPhone: document.getElementById('institutionPhone').value,
        institutionEmail: document.getElementById('institutionEmail').value
    };
    
    saveSettings(settings);
    showAlert('Institution settings saved successfully!', 'success');
}

// ============================================
// Save Email Settings
// ============================================
function saveEmailSettings() {
    const settings = {
        smtpServer: document.getElementById('smtpServer').value,
        smtpPort: document.getElementById('smtpPort').value,
        emailAddress: document.getElementById('emailAddress').value,
        emailNotifications: document.getElementById('emailNotifications').checked
    };
    
    saveSettings(settings);
    showAlert('Email settings saved successfully!', 'success');
}

// ============================================
// Change Password
// ============================================
function changePassword() {
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (!currentPassword) {
        showAlert('Please enter your current password', 'warning');
        return;
    }
    
    if (newPassword.length < 8) {
        showAlert('New password must be at least 8 characters', 'warning');
        return;
    }
    
    if (newPassword !== confirmPassword) {
        showAlert('Passwords do not match', 'danger');
        return;
    }
    
    // Here you would send to backend API
    showAlert('Password changed successfully!', 'success');
    
    // Clear fields
    document.getElementById('currentPassword').value = '';
    document.getElementById('newPassword').value = '';
    document.getElementById('confirmPassword').value = '';
    document.getElementById('passwordStrengthBar').className = 'bar';
    document.getElementById('passwordStrengthText').textContent = 'Password must be at least 8 characters';
}

// ============================================
// Logo Upload
// ============================================
function handleLogoUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!file.type.startsWith('image/')) {
        showAlert('Please upload an image file', 'warning');
        return;
    }
    
    if (file.size > 2 * 1024 * 1024) {
        showAlert('File size must be less than 2MB', 'warning');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const imageUrl = e.target.result;
        document.getElementById('logoImage').src = imageUrl;
        saveSettings({ logo: imageUrl });
        showAlert('Logo uploaded successfully!', 'success');
    };
    reader.readAsDataURL(file);
}

function removeLogo() {
    document.getElementById('logoImage').src = 'https://ui-avatars.com/api/?name=STTIMS&background=4F46E5&color=fff&size=120';
    saveSettings({ logo: null });
    showAlert('Logo removed successfully!', 'success');
}

// ============================================
// Theme Settings
// ============================================
function selectTheme(theme) {
    // Update UI
    document.querySelectorAll('.theme-option').forEach(el => {
        el.classList.remove('active');
    });
    document.querySelector(`.theme-option[data-theme="${theme}"]`).classList.add('active');
    
    // Apply theme
    const themeColors = {
        default: { primary: '#4F46E5', secondary: '#7C3AED' },
        dark: { primary: '#1F2937', secondary: '#374151' },
        light: { primary: '#F9FAFB', secondary: '#E5E7EB' },
        blue: { primary: '#1E40AF', secondary: '#3B82F6' },
        green: { primary: '#065F46', secondary: '#10B981' },
        purple: { primary: '#4C1D95', secondary: '#7C3AED' }
    };
    
    const colors = themeColors[theme] || themeColors.default;
    
    // Update navbar gradient
    const navbar = document.querySelector('.navbar.bg-primary');
    if (navbar) {
        navbar.style.background = `linear-gradient(135deg, ${colors.primary} 0%, ${colors.secondary} 100%)`;
    }
    
    // Update primary buttons
    document.querySelectorAll('.btn-primary').forEach(btn => {
        btn.style.background = `linear-gradient(135deg, ${colors.primary}, ${colors.secondary})`;
    });
    
    saveSettings({ theme: theme });
}

// ============================================
// Certificate Template
// ============================================
function updateTemplatePreview() {
    const template = document.getElementById('certificateTemplate').value;
    const preview = document.getElementById('templatePreview');
    
    const templates = {
        professional: { name: 'Professional Certificate', icon: 'fa-certificate', desc: 'Elegant and professional design' },
        modern: { name: 'Modern Certificate', icon: 'fa-award', desc: 'Clean and contemporary design' },
        classic: { name: 'Classic Certificate', icon: 'fa-scroll', desc: 'Traditional and timeless design' },
        executive: { name: 'Executive Certificate', icon: 'fa-crown', desc: 'Premium executive design' },
        minimal: { name: 'Minimal Certificate', icon: 'fa-certificate', desc: 'Simple and minimalist design' }
    };
    
    const templateData = templates[template] || templates.professional;
    
    preview.innerHTML = `
        <div class="template-icon">
            <i class="fas ${templateData.icon}"></i>
        </div>
        <div class="template-name">${templateData.name}</div>
        <div class="template-desc">${templateData.desc}</div>
    `;
    
    saveSettings({ certificateTemplate: template });
}

function previewTemplate() {
    const template = document.getElementById('certificateTemplate').value;
    const body = document.getElementById('templatePreviewBody');
    
    const templateHTML = `
        <div class="certificate-preview">
            <div class="cert-border">
                <div class="text-center">
                    <div class="cert-logo" style="width:60px;height:60px;background:#4F46E5;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;color:#fff;font-size:1.5rem;margin-bottom:1rem;">
                        <i class="fas fa-graduation-cap"></i>
                    </div>
                    <h2 class="cert-title" style="font-size:1.75rem;font-weight:700;color:#1F2937;">CERTIFICATE OF COMPLETION</h2>
                    <div class="cert-body" style="max-width:500px;margin:1rem auto;">
                        <p>This certificate is proudly presented to</p>
                        <h4 style="color:#4F46E5;font-weight:700;">John Doe</h4>
                        <p>for successfully completing the course</p>
                        <h5 style="font-weight:600;">Python Programming Fundamentals</h5>
                    </div>
                    <div class="cert-signatures" style="display:flex;justify-content:center;gap:2rem;margin-top:1.5rem;">
                        <div style="text-align:center;">
                            <div style="width:100px;height:2px;background:#1F2937;margin:0.5rem auto;"></div>
                            <div style="font-weight:600;">Dr. Abebe Kebede</div>
                            <div style="font-size:0.7rem;color:#6B7280;">Director of Training</div>
                        </div>
                        <div style="text-align:center;">
                            <div style="width:100px;height:2px;background:#1F2937;margin:0.5rem auto;"></div>
                            <div style="font-weight:600;">Eng. Tigist Hailu</div>
                            <div style="font-size:0.7rem;color:#6B7280;">Head of Department</div>
                        </div>
                    </div>
                    <div class="cert-footer" style="margin-top:1.5rem;font-size:0.7rem;color:#9CA3AF;">
                        Issued on: March 28, 2024
                    </div>
                </div>
            </div>
        </div>
    `;
    
    body.innerHTML = templateHTML;
    
    const modal = new bootstrap.Modal(document.getElementById('templatePreviewModal'));
    modal.show();
}

function applyTemplate() {
    const template = document.getElementById('certificateTemplate').value;
    saveSettings({ certificateTemplate: template });
    updateTemplatePreview();
    bootstrap.Modal.getInstance(document.getElementById('templatePreviewModal')).hide();
    showAlert(`Certificate template "${template}" applied successfully!`, 'success');
}

// ============================================
// Password Strength
// ============================================
function validatePasswordStrength() {
    const password = document.getElementById('newPassword').value;
    const bar = document.getElementById('passwordStrengthBar');
    const text = document.getElementById('passwordStrengthText');
    
    if (password.length === 0) {
        bar.className = 'bar';
        text.textContent = 'Password must be at least 8 characters';
        return;
    }
    
    let strength = 0;
    let level = 'weak';
    let message = 'Weak';
    
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    if (strength >= 5) { level = 'very-strong'; message = 'Very Strong'; }
    else if (strength >= 4) { level = 'strong'; message = 'Strong'; }
    else if (strength >= 3) { level = 'medium'; message = 'Medium'; }
    else { level = 'weak'; message = 'Weak'; }
    
    bar.className = 'bar ' + level;
    text.textContent = `Password strength: ${message}`;
}

// ============================================
// Save Settings
// ============================================
function saveSettings(newSettings) {
    const currentSettings = JSON.parse(localStorage.getItem('sttims_settings') || '{}');
    const updatedSettings = { ...currentSettings, ...newSettings };
    localStorage.setItem('sttims_settings', JSON.stringify(updatedSettings));
}

// ============================================
// Utility Functions
// ============================================
function showAlert(message, type = 'info') {
    const container = document.getElementById('alertContainer');
    const icons = {
        success: 'fa-check-circle',
        danger: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="fas ${icons[type] || icons.info} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    setTimeout(() => {
        const alert = container.querySelector('.alert');
        if (alert) {
            alert.classList.remove('show');
            setTimeout(() => container.innerHTML = '', 300);
        }
    }, 5000);
}

// ============================================
// Initialize on page load
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadSettings();
    updateTemplatePreview();
});
