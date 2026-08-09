// settings-api.js
// Settings API functions for STTIMS

/**
 * Get all settings
 * @returns {Promise} - { data: { institution, logo, theme, certificate_template, email, ... } }
 */
async function getSettings() {
    return await apiCall('/settings');
}

/**
 * Update institution settings
 * @param {object} data - { name, code, address, phone, email }
 * @returns {Promise} - Updated settings
 */
async function updateInstitutionSettings(data) {
    return await apiCall('/settings/institution', 'PUT', data);
}

/**
 * Upload institution logo
 * @param {File} file - Image file
 * @returns {Promise} - { logo_url: string }
 */
async function uploadLogo(file) {
    const formData = new FormData();
    formData.append('logo', file);
    
    const token = localStorage.getItem('authToken');
    const response = await fetch(`${API_BASE_URL}/settings/logo`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to upload logo');
    }
    
    return await response.json();
}

/**
 * Remove institution logo
 * @returns {Promise} - Success message
 */
async function removeLogo() {
    return await apiCall('/settings/logo', 'DELETE');
}

/**
 * Update theme settings
 * @param {string} theme - 'default', 'dark', 'light', 'blue', 'green', 'purple'
 * @returns {Promise} - Updated settings
 */
async function updateTheme(theme) {
    return await apiCall('/settings/theme', 'PUT', { theme });
}

/**
 * Update email settings
 * @param {object} data - { smtp_server, smtp_port, address, password, notifications_enabled }
 * @returns {Promise} - Updated settings
 */
async function updateEmailSettings(data) {
    return await apiCall('/settings/email', 'PUT', data);
}

/**
 * Update certificate template
 * @param {string} template - 'professional', 'modern', 'classic', 'executive', 'minimal'
 * @returns {Promise} - Updated settings
 */
async function updateCertificateTemplate(template) {
    return await apiCall('/settings/certificate-template', 'PUT', { template });
}

/**
 * Test email configuration
 * @param {string} testEmail - Email address to send test to
 * @returns {Promise} - { success: boolean, message: string }
 */
async function testEmailConfig(testEmail) {
    return await apiCall('/settings/email/test', 'POST', { test_email: testEmail });
}

/**
 * Change user password
 * @param {object} data - { current_password, new_password }
 * @returns {Promise} - Success message
 */
async function changePassword(data) {
    return await apiCall('/auth/change-password', 'POST', data);
}

/**
 * Get system information
 * @returns {Promise} - { version, php_version, mysql_version, server_time, ... }
 */
async function getSystemInfo() {
    return await apiCall('/settings/system-info');
}

/**
 * Clear system cache
 * @returns {Promise} - Success message
 */
async function clearCache() {
    return await apiCall('/settings/clear-cache', 'POST');
}

/**
 * Export system settings
 * @param {string} format - 'json' or 'xml' (default: 'json')
 * @returns {Promise} - Blob (file download)
 */
async function exportSettings(format = 'json') {
    return await apiCall(`/settings/export?format=${format}`);
}

/**
 * Import system settings
 * @param {File} file - JSON or XML file
 * @returns {Promise} - { imported: boolean, message: string }
 */
async function importSettings(file) {
    const formData = new FormData();
    formData.append('settings', file);
    
    const token = localStorage.getItem('authToken');
    const response = await fetch(`${API_BASE_URL}/settings/import`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to import settings');
    }
    
    return await response.json();
}

/**
 * Get audit log
 * @param {number} limit - Number of logs to retrieve (default: 50)
 * @param {string} dateFrom - Start date filter
 * @param {string} dateTo - End date filter
 * @returns {Promise} - Array of log entries
 */
async function getAuditLog(limit = 50, dateFrom = null, dateTo = null) {
    const params = new URLSearchParams({ limit });
    if (dateFrom) params.append('date_from', dateFrom);
    if (dateTo) params.append('date_to', dateTo);
    return await apiCall(`/settings/audit-log?${params.toString()}`);
}

// Export all functions for use in settings.html
window.SettingsAPI = {
    getSettings,
    updateInstitutionSettings,
    uploadLogo,
    removeLogo,
    updateTheme,
    updateEmailSettings,
    updateCertificateTemplate,
    testEmailConfig,
    changePassword,
    getSystemInfo,
    clearCache,
    exportSettings,
    importSettings,
    getAuditLog
};

console.log('⚙️ Settings API loaded successfully');
