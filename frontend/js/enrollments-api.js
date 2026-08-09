// enrollments-api.js
// Enrollment-specific API functions for STTIMS

/**
 * Get list of enrollments with pagination and filters
 * @param {number} page - Page number (default: 1)
 * @param {number} perPage - Items per page (default: 10)
 * @param {object} filters - Filter options (search, status, payment_status)
 * @returns {Promise} - { data: [...], total: number, total_pages: number }
 */
async function getEnrollments(page = 1, perPage = 10, filters = {}) {
    const params = new URLSearchParams({
        page: page,
        per_page: perPage,
        ...filters
    });
    return await apiCall(`/enrollments?${params.toString()}`);
}

/**
 * Get a single enrollment by ID
 * @param {number} id - Enrollment ID
 * @returns {Promise} - Enrollment object
 */
async function getEnrollment(id) {
    return await apiCall(`/enrollments/${id}`);
}

/**
 * Create a new enrollment
 * @param {object} data - Enrollment data (trainee_id, batch_id, payment_status, etc.)
 * @returns {Promise} - Created enrollment object
 */
async function createEnrollment(data) {
    return await apiCall('/enrollments', 'POST', data);
}

/**
 * Update an existing enrollment
 * @param {number} id - Enrollment ID
 * @param {object} data - Updated enrollment data
 * @returns {Promise} - Updated enrollment object
 */
async function updateEnrollment(id, data) {
    return await apiCall(`/enrollments/${id}`, 'PUT', data);
}

/**
 * Delete an enrollment
 * @param {number} id - Enrollment ID
 * @returns {Promise} - Success message
 */
async function deleteEnrollment(id) {
    return await apiCall(`/enrollments/${id}`, 'DELETE');
}

/**
 * Get all enrollments for a trainee
 * @param {number} traineeId - Trainee ID
 * @returns {Promise} - Array of enrollment objects
 */
async function getTraineeEnrollments(traineeId) {
    return await apiCall(`/enrollments/trainee/${traineeId}`);
}

/**
 * Get all enrollments for a batch
 * @param {number} batchId - Batch ID
 * @returns {Promise} - Array of enrollment objects
 */
async function getBatchEnrollments(batchId) {
    return await apiCall(`/enrollments/batch/${batchId}`);
}

/**
 * Update enrollment status
 * @param {number} id - Enrollment ID
 * @param {string} status - 'Enrolled', 'Active', 'Completed', 'Dropped', 'Suspended'
 * @returns {Promise} - Updated enrollment object
 */
async function updateEnrollmentStatus(id, status) {
    return await apiCall(`/enrollments/${id}/status`, 'PATCH', { status });
}

/**
 * Update payment status
 * @param {number} id - Enrollment ID
 * @param {string} paymentStatus - 'Paid', 'Pending', 'Partial', 'Scholarship'
 * @param {number} amount - Payment amount
 * @returns {Promise} - Updated enrollment object
 */
async function updatePaymentStatus(id, paymentStatus, amount = null) {
    const data = { payment_status: paymentStatus };
    if (amount !== null) data.amount_paid = amount;
    return await apiCall(`/enrollments/${id}/payment`, 'PATCH', data);
}

/**
 * Get enrollment statistics
 * @param {number} id - Enrollment ID
 * @returns {Promise} - { attendance_percentage, grade, completion_status }
 */
async function getEnrollmentStatistics(id) {
    return await apiCall(`/enrollments/${id}/statistics`);
}

/**
 * Check if trainee is already enrolled in a batch
 * @param {number} traineeId - Trainee ID
 * @param {number} batchId - Batch ID
 * @returns {Promise} - { enrolled: boolean, enrollment_id: number }
 */
async function checkDuplicateEnrollment(traineeId, batchId) {
    return await apiCall(`/enrollments/check?trainee_id=${traineeId}&batch_id=${batchId}`);
}

/**
 * Export enrollments data
 * @param {string} format - 'csv' or 'pdf' (default: 'csv')
 * @param {object} filters - Filter options
 * @returns {Promise} - Blob (file download)
 */
async function exportEnrollments(format = 'csv', filters = {}) {
    const params = new URLSearchParams({
        format: format,
        ...filters
    });
    return await apiCall(`/enrollments/export?${params.toString()}`);
}

/**
 * Bulk enroll trainees
 * @param {number} batchId - Batch ID
 * @param {array} traineeIds - Array of trainee IDs
 * @returns {Promise} - { enrolled: number, failed: number, errors: [...] }
 */
async function bulkEnroll(batchId, traineeIds) {
    return await apiCall('/enrollments/bulk', 'POST', {
        batch_id: batchId,
        trainee_ids: traineeIds
    });
}

/**
 * Get enrollment payment history
 * @param {number} id - Enrollment ID
 * @returns {Promise} - Array of payment records
 */
async function getEnrollmentPayments(id) {
    return await apiCall(`/enrollments/${id}/payments`);
}

/**
 * Generate certificate for enrollment
 * @param {number} id - Enrollment ID
 * @returns {Promise} - Certificate object
 */
async function generateCertificate(id) {
    return await apiCall(`/enrollments/${id}/certificate`, 'POST');
}

// Export all functions for use in enrollments.html
window.EnrollmentsAPI = {
    getEnrollments,
    getEnrollment,
    createEnrollment,
    updateEnrollment,
    deleteEnrollment,
    getTraineeEnrollments,
    getBatchEnrollments,
    updateEnrollmentStatus,
    updatePaymentStatus,
    getEnrollmentStatistics,
    checkDuplicateEnrollment,
    exportEnrollments,
    bulkEnroll,
    getEnrollmentPayments,
    generateCertificate
};

console.log('📋 Enrollments API loaded successfully');
