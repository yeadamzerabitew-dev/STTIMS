// sessions-api.js
// Class Session API functions for STTIMS

/**
 * Get list of class sessions with pagination and filters
 * @param {number} page - Page number (default: 1)
 * @param {number} perPage - Items per page (default: 10)
 * @param {object} filters - Filter options (search, batch_id, status)
 * @returns {Promise} - { data: [...], total: number, total_pages: number }
 */
async function getSessions(page = 1, perPage = 10, filters = {}) {
    const params = new URLSearchParams({
        page: page,
        per_page: perPage,
        ...filters
    });
    return await apiCall(`/sessions?${params.toString()}`);
}

/**
 * Get a single session by ID
 * @param {number} id - Session ID
 * @returns {Promise} - Session object
 */
async function getSession(id) {
    return await apiCall(`/sessions/${id}`);
}

/**
 * Create a new class session
 * @param {object} data - Session data (batch_id, instructor_id, session_date, etc.)
 * @returns {Promise} - Created session object
 */
async function createSession(data) {
    return await apiCall('/sessions', 'POST', data);
}

/**
 * Update an existing session
 * @param {number} id - Session ID
 * @param {object} data - Updated session data
 * @returns {Promise} - Updated session object
 */
async function updateSession(id, data) {
    return await apiCall(`/sessions/${id}`, 'PUT', data);
}

/**
 * Delete a session
 * @param {number} id - Session ID
 * @returns {Promise} - Success message
 */
async function deleteSession(id) {
    return await apiCall(`/sessions/${id}`, 'DELETE');
}

/**
 * Get all sessions for a batch
 * @param {number} batchId - Batch ID
 * @returns {Promise} - Array of session objects
 */
async function getBatchSessions(batchId) {
    return await apiCall(`/sessions/batch/${batchId}`);
}

/**
 * Get all sessions for an instructor
 * @param {number} instructorId - Instructor ID
 * @param {string} dateFrom - Start date filter (optional)
 * @param {string} dateTo - End date filter (optional)
 * @returns {Promise} - Array of session objects
 */
async function getInstructorSessions(instructorId, dateFrom = null, dateTo = null) {
    const params = new URLSearchParams();
    if (dateFrom) params.append('date_from', dateFrom);
    if (dateTo) params.append('date_to', dateTo);
    return await apiCall(`/sessions/instructor/${instructorId}?${params.toString()}`);
}

/**
 * Update session status
 * @param {number} id - Session ID
 * @param {string} status - 'Scheduled', 'Ongoing', 'Completed', 'Cancelled'
 * @returns {Promise} - Updated session object
 */
async function updateSessionStatus(id, status) {
    return await apiCall(`/sessions/${id}/status`, 'PATCH', { status });
}

/**
 * Get attendance for a session
 * @param {number} id - Session ID
 * @returns {Promise} - Array of attendance records
 */
async function getSessionAttendance(id) {
    return await apiCall(`/sessions/${id}/attendance`);
}

/**
 * Mark attendance for a session
 * @param {number} id - Session ID
 * @param {array} attendance - Array of { trainee_id, status, remarks }
 * @returns {Promise} - Success message
 */
async function markSessionAttendance(id, attendance) {
    return await apiCall(`/sessions/${id}/attendance`, 'POST', { attendance });
}

/**
 * Get upcoming sessions
 * @param {number} limit - Number of sessions to retrieve (default: 5)
 * @returns {Promise} - Array of upcoming sessions
 */
async function getUpcomingSessions(limit = 5) {
    return await apiCall(`/sessions/upcoming?limit=${limit}`);
}

/**
 * Get session statistics
 * @param {number} id - Session ID
 * @returns {Promise} - { total_present, total_absent, total_late, attendance_rate }
 */
async function getSessionStatistics(id) {
    return await apiCall(`/sessions/${id}/statistics`);
}

/**
 * Export sessions data
 * @param {string} format - 'csv' or 'pdf' (default: 'csv')
 * @param {object} filters - Filter options
 * @returns {Promise} - Blob (file download)
 */
async function exportSessions(format = 'csv', filters = {}) {
    const params = new URLSearchParams({
        format: format,
        ...filters
    });
    return await apiCall(`/sessions/export?${params.toString()}`);
}

/**
 * Bulk create sessions for a batch
 * @param {number} batchId - Batch ID
 * @param {array} sessions - Array of session data objects
 * @returns {Promise} - { created: number, failed: number, errors: [...] }
 */
async function bulkCreateSessions(batchId, sessions) {
    return await apiCall('/sessions/bulk', 'POST', {
        batch_id: batchId,
        sessions: sessions
    });
}

/**
 * Get session schedule for a date range
 * @param {string} dateFrom - Start date
 * @param {string} dateTo - End date
 * @param {number} batchId - Optional batch filter
 * @returns {Promise} - Array of session objects
 */
async function getSessionSchedule(dateFrom, dateTo, batchId = null) {
    const params = new URLSearchParams({
        date_from: dateFrom,
        date_to: dateTo
    });
    if (batchId) params.append('batch_id', batchId);
    return await apiCall(`/sessions/schedule?${params.toString()}`);
}

// Export all functions for use in sessions.html
window.SessionsAPI = {
    getSessions,
    getSession,
    createSession,
    updateSession,
    deleteSession,
    getBatchSessions,
    getInstructorSessions,
    updateSessionStatus,
    getSessionAttendance,
    markSessionAttendance,
    getUpcomingSessions,
    getSessionStatistics,
    exportSessions,
    bulkCreateSessions,
    getSessionSchedule
};

console.log('🕐 Sessions API loaded successfully');
