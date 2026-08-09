// batches-api.js
// Batch-specific API functions for STTIMS

/**
 * Get list of batches with pagination and filters
 * @param {number} page - Page number (default: 1)
 * @param {number} perPage - Items per page (default: 10)
 * @param {object} filters - Filter options (search, course_id, status)
 * @returns {Promise} - { data: [...], total: number, total_pages: number }
 */
async function getBatches(page = 1, perPage = 10, filters = {}) {
    const params = new URLSearchParams({
        page: page,
        per_page: perPage,
        ...filters
    });
    return await apiCall(`/batches?${params.toString()}`);
}

/**
 * Get a single batch by ID
 * @param {number} id - Batch ID
 * @returns {Promise} - Batch object
 */
async function getBatch(id) {
    return await apiCall(`/batches/${id}`);
}

/**
 * Create a new batch
 * @param {object} data - Batch data (batch_name, course_id, start_date, end_date, etc.)
 * @returns {Promise} - Created batch object
 */
async function createBatch(data) {
    return await apiCall('/batches', 'POST', data);
}

/**
 * Update an existing batch
 * @param {number} id - Batch ID
 * @param {object} data - Updated batch data
 * @returns {Promise} - Updated batch object
 */
async function updateBatch(id, data) {
    return await apiCall(`/batches/${id}`, 'PUT', data);
}

/**
 * Delete a batch
 * @param {number} id - Batch ID
 * @returns {Promise} - Success message
 */
async function deleteBatch(id) {
    return await apiCall(`/batches/${id}`, 'DELETE');
}

/**
 * Get all enrollments for a batch
 * @param {number} id - Batch ID
 * @returns {Promise} - Array of enrollment objects
 */
async function getBatchEnrollments(id) {
    return await apiCall(`/batches/${id}/enrollments`);
}

/**
 * Get all class sessions for a batch
 * @param {number} id - Batch ID
 * @returns {Promise} - Array of session objects
 */
async function getBatchSessions(id) {
    return await apiCall(`/batches/${id}/sessions`);
}

/**
 * Get all assessments for a batch
 * @param {number} id - Batch ID
 * @returns {Promise} - Array of assessment objects
 */
async function getBatchAssessments(id) {
    return await apiCall(`/batches/${id}/assessments`);
}

/**
 * Get batch statistics
 * @param {number} id - Batch ID
 * @returns {Promise} - { total_enrollments, attendance_rate, completion_rate, avg_score }
 */
async function getBatchStatistics(id) {
    return await apiCall(`/batches/${id}/statistics`);
}

/**
 * Update batch status
 * @param {number} id - Batch ID
 * @param {string} status - 'Upcoming', 'Ongoing', 'Completed', or 'Cancelled'
 * @returns {Promise} - Updated batch object
 */
async function updateBatchStatus(id, status) {
    return await apiCall(`/batches/${id}/status`, 'PATCH', { status });
}

/**
 * Get available batches for a course
 * @param {number} courseId - Course ID
 * @returns {Promise} - Array of available batches
 */
async function getAvailableBatches(courseId) {
    return await apiCall(`/batches/available?course_id=${courseId}`);
}

/**
 * Export batches data
 * @param {string} format - 'csv' or 'pdf' (default: 'csv')
 * @param {object} filters - Filter options
 * @returns {Promise} - Blob (file download)
 */
async function exportBatches(format = 'csv', filters = {}) {
    const params = new URLSearchParams({
        format: format,
        ...filters
    });
    return await apiCall(`/batches/export?${params.toString()}`);
}

/**
 * Get upcoming batches
 * @param {number} limit - Number of batches to retrieve (default: 5)
 * @returns {Promise} - Array of upcoming batches
 */
async function getUpcomingBatches(limit = 5) {
    return await apiCall(`/batches/upcoming?limit=${limit}`);
}

/**
 * Check if batch has capacity
 * @param {number} id - Batch ID
 * @returns {Promise} - { has_capacity: boolean, available_slots: number }
 */
async function checkBatchCapacity(id) {
    return await apiCall(`/batches/${id}/capacity`);
}

/**
 * Clone a batch
 * @param {number} id - Batch ID to clone
 * @param {object} data - Override data for new batch
 * @returns {Promise} - Created batch object
 */
async function cloneBatch(id, data = {}) {
    return await apiCall(`/batches/${id}/clone`, 'POST', data);
}

// Export all functions for use in batches.html
window.BatchesAPI = {
    getBatches,
    getBatch,
    createBatch,
    updateBatch,
    deleteBatch,
    getBatchEnrollments,
    getBatchSessions,
    getBatchAssessments,
    getBatchStatistics,
    updateBatchStatus,
    getAvailableBatches,
    exportBatches,
    getUpcomingBatches,
    checkBatchCapacity,
    cloneBatch
};

console.log('📦 Batches API loaded successfully');
