// attendance-api.js
// Attendance API functions for STTIMS

/**
 * Get attendance records with pagination and filters
 * @param {number} page - Page number (default: 1)
 * @param {number} perPage - Items per page (default: 10)
 * @param {object} filters - Filter options (search, batch_id, session_id, status)
 * @returns {Promise} - { data: [...], total: number, total_pages: number }
 */
async function getAttendance(page = 1, perPage = 10, filters = {}) {
    const params = new URLSearchParams({
        page: page,
        per_page: perPage,
        ...filters
    });
    return await apiCall(`/attendance?${params.toString()}`);
}

/**
 * Get attendance for a specific session
 * @param {number} sessionId - Session ID
 * @returns {Promise} - Array of attendance records
 */
async function getSessionAttendance(sessionId) {
    return await apiCall(`/sessions/${sessionId}/attendance`);
}

/**
 * Mark attendance for a session
 * @param {number} sessionId - Session ID
 * @param {array} attendance - Array of { trainee_id, status, remarks }
 * @returns {Promise} - Success message
 */
async function markSessionAttendance(sessionId, attendance) {
    return await apiCall(`/sessions/${sessionId}/attendance`, 'POST', { attendance });
}

/**
 * Get attendance for a specific trainee
 * @param {number} traineeId - Trainee ID
 * @param {string} dateFrom - Start date filter (optional)
 * @param {string} dateTo - End date filter (optional)
 * @returns {Promise} - Array of attendance records
 */
async function getTraineeAttendance(traineeId, dateFrom = null, dateTo = null) {
    const params = new URLSearchParams();
    if (dateFrom) params.append('date_from', dateFrom);
    if (dateTo) params.append('date_to', dateTo);
    return await apiCall(`/attendance/trainee/${traineeId}?${params.toString()}`);
}

/**
 * Update attendance status for a trainee
 * @param {number} attendanceId - Attendance record ID
 * @param {string} status - 'Present', 'Absent', 'Late', 'Excused'
 * @param {string} remarks - Optional remarks
 * @returns {Promise} - Updated attendance record
 */
async function updateAttendanceStatus(attendanceId, status, remarks = null) {
    const data = { status };
    if (remarks !== null) data.remarks = remarks;
    return await apiCall(`/attendance/${attendanceId}`, 'PATCH', data);
}

/**
 * Get attendance statistics
 * @param {object} filters - Filter options (batch_id, session_id, trainee_id, date_from, date_to)
 * @returns {Promise} - { total_present, total_absent, total_late, total_excused, total_records }
 */
async function getAttendanceStatistics(filters = {}) {
    const params = new URLSearchParams(filters);
    return await apiCall(`/attendance/statistics?${params.toString()}`);
}

/**
 * Get attendance summary for a batch
 * @param {number} batchId - Batch ID
 * @returns {Promise} - { total_sessions, attended_sessions, missed_sessions, attendance_rate }
 */
async function getBatchAttendanceSummary(batchId) {
    return await apiCall(`/attendance/batch/${batchId}/summary`);
}

/**
 * Get attendance summary for a trainee
 * @param {number} traineeId - Trainee ID
 * @param {number} batchId - Optional batch filter
 * @returns {Promise} - { total_sessions, present, absent, late, excused, attendance_rate }
 */
async function getTraineeAttendanceSummary(traineeId, batchId = null) {
    const params = new URLSearchParams();
    if (batchId) params.append('batch_id', batchId);
    return await apiCall(`/attendance/trainee/${traineeId}/summary?${params.toString()}`);
}

/**
 * Export attendance data
 * @param {string} format - 'csv' or 'pdf' (default: 'csv')
 * @param {object} filters - Filter options
 * @returns {Promise} - Blob (file download)
 */
async function exportAttendance(format = 'csv', filters = {}) {
    const params = new URLSearchParams({
        format: format,
        ...filters
    });
    return await apiCall(`/attendance/export?${params.toString()}`);
}

/**
 * Get attendance by date range
 * @param {string} dateFrom - Start date
 * @param {string} dateTo - End date
 * @param {number} batchId - Optional batch filter
 * @returns {Promise} - Array of attendance records
 */
async function getAttendanceByDateRange(dateFrom, dateTo, batchId = null) {
    const params = new URLSearchParams({
        date_from: dateFrom,
        date_to: dateTo
    });
    if (batchId) params.append('batch_id', batchId);
    return await apiCall(`/attendance/date-range?${params.toString()}`);
}

/**
 * Bulk update attendance status
 * @param {array} updates - Array of { attendance_id, status, remarks }
 * @returns {Promise} - { updated: number, failed: number, errors: [...] }
 */
async function bulkUpdateAttendance(updates) {
    return await apiCall('/attendance/bulk', 'PATCH', { updates });
}

// Export all functions for use in attendance.html
window.AttendanceAPI = {
    getAttendance,
    getSessionAttendance,
    markSessionAttendance,
    getTraineeAttendance,
    updateAttendanceStatus,
    getAttendanceStatistics,
    getBatchAttendanceSummary,
    getTraineeAttendanceSummary,
    exportAttendance,
    getAttendanceByDateRange,
    bulkUpdateAttendance
};

console.log('📋 Attendance API loaded successfully');
