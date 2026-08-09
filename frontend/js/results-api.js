// results-api.js
// Results API functions for STTIMS

/**
 * Get results with pagination and filters
 * @param {number} page - Page number (default: 1)
 * @param {number} perPage - Items per page (default: 10)
 * @param {object} filters - Filter options (assessment_id, trainee_id, status)
 * @returns {Promise} - { data: [...], total: number, total_pages: number }
 */
async function getResults(page = 1, perPage = 10, filters = {}) {
    const params = new URLSearchParams({
        page: page,
        per_page: perPage,
        ...filters
    });
    return await apiCall(`/results?${params.toString()}`);
}

/**
 * Get results for a specific assessment
 * @param {number} assessmentId - Assessment ID
 * @returns {Promise} - Array of result objects
 */
async function getAssessmentResults(assessmentId) {
    return await apiCall(`/assessments/${assessmentId}/results`);
}

/**
 * Get results for a specific trainee
 * @param {number} traineeId - Trainee ID
 * @param {number} batchId - Optional batch filter
 * @returns {Promise} - Array of result objects
 */
async function getTraineeResults(traineeId, batchId = null) {
    const params = new URLSearchParams();
    if (batchId) params.append('batch_id', batchId);
    return await apiCall(`/results/trainee/${traineeId}?${params.toString()}`);
}

/**
 * Submit results for an assessment
 * @param {number} assessmentId - Assessment ID
 * @param {array} results - Array of { trainee_id, marks_obtained, feedback }
 * @returns {Promise} - Success message
 */
async function submitResults(assessmentId, results) {
    return await apiCall(`/assessments/${assessmentId}/results`, 'POST', { results });
}

/**
 * Update a single result
 * @param {number} resultId - Result ID
 * @param {object} data - Updated result data (marks_obtained, feedback, status)
 * @returns {Promise} - Updated result object
 */
async function updateResult(resultId, data) {
    return await apiCall(`/results/${resultId}`, 'PATCH', data);
}

/**
 * Get grade scale
 * @returns {Promise} - Array of grade objects
 */
async function getGradeScale() {
    return await apiCall('/grade-scale');
}

/**
 * Get grade for a percentage score
 * @param {number} percentage - Percentage score
 * @returns {Promise} - { grade: string, is_pass: boolean }
 */
async function getGradeByPercentage(percentage) {
    return await apiCall(`/grade-scale/grade?percentage=${percentage}`);
}

/**
 * Get result statistics for an assessment
 * @param {number} assessmentId - Assessment ID
 * @returns {Promise} - { total_trainees, pass_count, fail_count, not_attempted, average_marks, max_marks, min_marks }
 */
async function getResultStatistics(assessmentId) {
    return await apiCall(`/assessments/${assessmentId}/results/statistics`);
}

/**
 * Get result summary for a trainee
 * @param {number} traineeId - Trainee ID
 * @param {number} batchId - Optional batch filter
 * @returns {Promise} - { total_assessments, completed, average_score, grades: [...] }
 */
async function getTraineeResultSummary(traineeId, batchId = null) {
    const params = new URLSearchParams();
    if (batchId) params.append('batch_id', batchId);
    return await apiCall(`/results/trainee/${traineeId}/summary?${params.toString()}`);
}

/**
 * Export results data
 * @param {string} format - 'csv' or 'pdf' (default: 'csv')
 * @param {object} filters - Filter options
 * @returns {Promise} - Blob (file download)
 */
async function exportResults(format = 'csv', filters = {}) {
    const params = new URLSearchParams({
        format: format,
        ...filters
    });
    return await apiCall(`/results/export?${params.toString()}`);
}

/**
 * Bulk update results
 * @param {array} updates - Array of { result_id, marks_obtained, feedback }
 * @returns {Promise} - { updated: number, failed: number, errors: [...] }
 */
async function bulkUpdateResults(updates) {
    return await apiCall('/results/bulk', 'PATCH', { updates });
}

/**
 * Get assessment result for a specific trainee
 * @param {number} traineeId - Trainee ID
 * @param {number} assessmentId - Assessment ID
 * @returns {Promise} - Result object
 */
async function getTraineeAssessmentResult(traineeId, assessmentId) {
    return await apiCall(`/results/trainee/${traineeId}/assessment/${assessmentId}`);
}

/**
 * Calculate final grade for a trainee in a batch
 * @param {number} traineeId - Trainee ID
 * @param {number} batchId - Batch ID
 * @returns {Promise} - { final_grade, overall_percentage, status }
 */
async function calculateFinalGrade(traineeId, batchId) {
    return await apiCall(`/results/final-grade?trainee_id=${traineeId}&batch_id=${batchId}`);
}

// Export all functions for use in results.html
window.ResultsAPI = {
    getResults,
    getAssessmentResults,
    getTraineeResults,
    submitResults,
    updateResult,
    getGradeScale,
    getGradeByPercentage,
    getResultStatistics,
    getTraineeResultSummary,
    exportResults,
    bulkUpdateResults,
    getTraineeAssessmentResult,
    calculateFinalGrade
};

console.log('📊 Results API loaded successfully');
