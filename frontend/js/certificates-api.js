// certificates-api.js
// Certificate API functions for STTIMS

/**
 * Get list of certificates with pagination and filters
 * @param {number} page - Page number (default: 1)
 * @param {number} perPage - Items per page (default: 10)
 * @param {object} filters - Filter options (search, status, trainee_id)
 * @returns {Promise} - { data: [...], total: number, total_pages: number }
 */
async function getCertificates(page = 1, perPage = 10, filters = {}) {
    const params = new URLSearchParams({
        page: page,
        per_page: perPage,
        ...filters
    });
    return await apiCall(`/certificates?${params.toString()}`);
}

/**
 * Get a single certificate by ID
 * @param {number} id - Certificate ID
 * @returns {Promise} - Certificate object
 */
async function getCertificate(id) {
    return await apiCall(`/certificates/${id}`);
}

/**
 * Create a new certificate
 * @param {object} data - Certificate data (enrollment_id, issue_date, expiry_date, notes)
 * @returns {Promise} - Created certificate object
 */
async function createCertificate(data) {
    return await apiCall('/certificates', 'POST', data);
}

/**
 * Update an existing certificate
 * @param {number} id - Certificate ID
 * @param {object} data - Updated certificate data
 * @returns {Promise} - Updated certificate object
 */
async function updateCertificate(id, data) {
    return await apiCall(`/certificates/${id}`, 'PUT', data);
}

/**
 * Delete a certificate
 * @param {number} id - Certificate ID
 * @returns {Promise} - Success message
 */
async function deleteCertificate(id) {
    return await apiCall(`/certificates/${id}`, 'DELETE');
}

/**
 * Get certificates for a trainee
 * @param {number} traineeId - Trainee ID
 * @returns {Promise} - Array of certificate objects
 */
async function getTraineeCertificates(traineeId) {
    return await apiCall(`/certificates/trainee/${traineeId}`);
}

/**
 * Get certificates for a course
 * @param {number} courseId - Course ID
 * @returns {Promise} - Array of certificate objects
 */
async function getCourseCertificates(courseId) {
    return await apiCall(`/certificates/course/${courseId}`);
}

/**
 * Update certificate status
 * @param {number} id - Certificate ID
 * @param {string} status - 'Issued', 'Revoked', 'Expired', 'Pending'
 * @returns {Promise} - Updated certificate object
 */
async function updateCertificateStatus(id, status) {
    return await apiCall(`/certificates/${id}/status`, 'PATCH', { status });
}

/**
 * Verify certificate by token
 * @param {string} token - Verification token
 * @returns {Promise} - { valid: boolean, certificate: object }
 */
async function verifyCertificate(token) {
    return await apiCall(`/certificates/verify/${token}`);
}

/**
 * Get certificate template settings
 * @param {number} courseId - Optional course ID
 * @returns {Promise} - Template settings object
 */
async function getCertificateTemplate(courseId = null) {
    const params = new URLSearchParams();
    if (courseId) params.append('course_id', courseId);
    return await apiCall(`/certificates/template?${params.toString()}`);
}

/**
 * Update certificate template
 * @param {object} data - Template settings
 * @returns {Promise} - Updated template settings
 */
async function updateCertificateTemplate(data) {
    return await apiCall('/certificates/template', 'PUT', data);
}

/**
 * Export certificates data
 * @param {string} format - 'csv' or 'pdf' (default: 'csv')
 * @param {object} filters - Filter options
 * @returns {Promise} - Blob (file download)
 */
async function exportCertificates(format = 'csv', filters = {}) {
    const params = new URLSearchParams({
        format: format,
        ...filters
    });
    return await apiCall(`/certificates/export?${params.toString()}`);
}

/**
 * Bulk generate certificates
 * @param {array} enrollments - Array of enrollment IDs
 * @param {object} options - Issue date, expiry date, etc.
 * @returns {Promise} - { generated: number, failed: number, errors: [...] }
 */
async function bulkGenerateCertificates(enrollments, options = {}) {
    return await apiCall('/certificates/bulk', 'POST', {
        enrollments: enrollments,
        ...options
    });
}

/**
 * Get certificate statistics
 * @param {object} filters - Filter options (date_from, date_to, course_id)
 * @returns {Promise} - { total_issued, total_pending, total_revoked, total_expired }
 */
async function getCertificateStatistics(filters = {}) {
    const params = new URLSearchParams(filters);
    return await apiCall(`/certificates/statistics?${params.toString()}`);
}

/**
 * Send certificate via email
 * @param {number} id - Certificate ID
 * @param {string} email - Email address
 * @returns {Promise} - Success message
 */
async function sendCertificateEmail(id, email) {
    return await apiCall(`/certificates/${id}/send`, 'POST', { email });
}

// Export all functions for use in certificates.html
window.CertificatesAPI = {
    getCertificates,
    getCertificate,
    createCertificate,
    updateCertificate,
    deleteCertificate,
    getTraineeCertificates,
    getCourseCertificates,
    updateCertificateStatus,
    verifyCertificate,
    getCertificateTemplate,
    updateCertificateTemplate,
    exportCertificates,
    bulkGenerateCertificates,
    getCertificateStatistics,
    sendCertificateEmail
};

console.log('🎓 Certificates API loaded successfully');
