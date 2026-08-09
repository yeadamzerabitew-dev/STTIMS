// assessments-api.js
// Assessment API functions for STTIMS

/**
 * Get list of assessments with pagination and filters
 * @param {number} page - Page number (default: 1)
 * @param {number} perPage - Items per page (default: 10)
 * @param {object} filters - Filter options (search, assessment_type, status, batch_id)
 * @returns {Promise} - { data: [...], total: number, total_pages: number }
 */
async function getAssessments(page = 1, perPage = 10, filters = {}) {
    const params = new URLSearchParams({
        page: page,
        per_page: perPage,
        ...filters
    });
    return await apiCall(`/assessments?${params.toString()}`);
}

/**
 * Get a single assessment by ID
 * @param {number} id - Assessment ID
 * @returns {Promise} - Assessment object
 */
async function getAssessment(id) {
    return await apiCall(`/assessments/${id}`);
}

/**
 * Create a new assessment
 * @param {object} data - Assessment data (title, type, batch_id, max_marks, etc.)
 * @returns {Promise} - Created assessment object
 */
async function createAssessment(data) {
    return await apiCall('/assessments', 'POST', data);
}

/**
 * Update an existing assessment
 * @param {number} id - Assessment ID
 * @param {object} data - Updated assessment data
 * @returns {Promise} - Updated assessment object
 */
async function updateAssessment(id, data) {
    return await apiCall(`/assessments/${id}`, 'PUT', data);
}

/**
 * Delete an assessment
 * @param {number} id - Assessment ID
 * @returns {Promise} - Success message
 */
async function deleteAssessment(id) {
    return await apiCall(`/assessments/${id}`, 'DELETE');
}

/**
 * Get all assessments for a batch
 * @param {number} batchId - Batch ID
 * @returns {Promise} - Array of assessment objects
 */
async function getBatchAssessments(batchId) {
    return await apiCall(`/assessments/batch/${batchId}`);
}

/**
 * Get results for an assessment
 * @param {number} id - Assessment ID
 * @returns {Promise} - Array of result objects
 */
async function getAssessmentResults(id) {
    return await apiCall(`/assessments/${id}/results`);
}

/**
 * Submit results for an assessment
 * @param {number} id - Assessment ID
 * @param {array} results - Array of { trainee_id, marks_obtained, feedback }
 * @returns {Promise} - Success message
 */
async function submitAssessmentResults(id, results) {
    return await apiCall(`/assessments/${id}/results`, 'POST', { results });
}

/**
 * Update assessment status
 * @param {number} id - Assessment ID
 * @param {string} status - 'Scheduled', 'Ongoing', 'Completed', 'Cancelled'
 * @returns {Promise} - Updated assessment object
 */
async function updateAssessmentStatus(id, status) {
    return await apiCall(`/assessments/${id}/status`, 'PATCH', { status });
}

/**
 * Get assessment statistics
 * @param {number} id - Assessment ID
 * @returns {Promise} - { total_trainees, average_score, pass_rate, max_score, min_score }
 */
async function getAssessmentStatistics(id) {
    return await apiCall(`/assessments/${id}/statistics`);
}

/**
 * Get weightage summary for a batch
 * @param {number} batchId - Batch ID
 * @returns {Promise} - { total_weightage, remaining_weightage, assessments: [...] }
 */
async function getBatchWeightageSummary(batchId) {
    return await apiCall(`/assessments/batch/${batchId}/weightage`);
}

/**
 * Export assessments data
 * @param {string} format - 'csv' or 'pdf' (default: 'csv')
 * @param {object} filters - Filter options
 * @returns {Promise} - Blob (file download)
 */
async function exportAssessments(format = 'csv', filters = {}) {
    const params = new URLSearchParams({
        format: format,
        ...filters
    });
    return await apiCall(`/assessments/export?${params.toString()}`);
}

/**
 * Bulk create assessments for a batch
 * @param {number} batchId - Batch ID
 * @param {array} assessments - Array of assessment data objects
 * @returns {Promise} - { created: number, failed: number, errors: [...] }
 */
async function bulkCreateAssessments(batchId, assessments) {
    return await apiCall('/assessments/bulk', 'POST', {
        batch_id: batchId,
        assessments: assessments
    });
}

/**
 * Get upcoming assessments
 * @param {number} limit - Number of assessments to retrieve (default: 5)
 * @returns {Promise} - Array of upcoming assessments
 */
async function getUpcomingAssessments(limit = 5) {
    return await apiCall(`/assessments/upcoming?limit=${limit}`);
}

// Export all functions for use in assessments.html
window.AssessmentsAPI = {
    getAssessments,
    getAssessment,
    createAssessment,
    updateAssessment,
    deleteAssessment,
    getBatchAssessments,
    getAssessmentResults,
    submitAssessmentResults,
    updateAssessmentStatus,
    getAssessmentStatistics,
    getBatchWeightageSummary,
    exportAssessments,
    bulkCreateAssessments,
    getUpcomingAssessments
};

console.log('📝 Assessments API loaded successfully');
