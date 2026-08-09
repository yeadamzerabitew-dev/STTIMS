// reports-api.js
// Reports API functions for STTIMS

/**
 * Get enrollment report data
 * @param {object} filters - Filter options (date_from, date_to, course_id)
 * @returns {Promise} - { summary: {...}, details: [...], charts: [...] }
 */
async function getEnrollmentReport(filters = {}) {
    const params = new URLSearchParams(filters);
    return await apiCall(`/reports/enrollment?${params.toString()}`);
}

/**
 * Get attendance report data
 * @param {object} filters - Filter options (date_from, date_to, batch_id)
 * @returns {Promise} - { summary: {...}, details: [...], charts: [...] }
 */
async function getAttendanceReport(filters = {}) {
    const params = new URLSearchParams(filters);
    return await apiCall(`/reports/attendance?${params.toString()}`);
}

/**
 * Get assessment report data
 * @param {object} filters - Filter options (date_from, date_to, batch_id)
 * @returns {Promise} - { summary: {...}, details: [...], charts: [...] }
 */
async function getAssessmentReport(filters = {}) {
    const params = new URLSearchParams(filters);
    return await apiCall(`/reports/assessment?${params.toString()}`);
}

/**
 * Get revenue report data
 * @param {object} filters - Filter options (date_from, date_to)
 * @returns {Promise} - { summary: {...}, details: [...], charts: [...] }
 */
async function getRevenueReport(filters = {}) {
    const params = new URLSearchParams(filters);
    return await apiCall(`/reports/revenue?${params.toString()}`);
}

/**
 * Get certificate report data
 * @param {object} filters - Filter options (date_from, date_to, course_id)
 * @returns {Promise} - { summary: {...}, details: [...], charts: [...] }
 */
async function getCertificateReport(filters = {}) {
    const params = new URLSearchParams(filters);
    return await apiCall(`/reports/certificate?${params.toString()}`);
}

/**
 * Get instructor report data
 * @param {object} filters - Filter options (date_from, date_to)
 * @returns {Promise} - { summary: {...}, details: [...], charts: [...] }
 */
async function getInstructorReport(filters = {}) {
    const params = new URLSearchParams(filters);
    return await apiCall(`/reports/instructor?${params.toString()}`);
}

/**
 * Get custom report data
 * @param {string} reportType - Type of report
 * @param {object} filters - Filter options
 * @returns {Promise} - { data: [...] }
 */
async function getCustomReport(reportType, filters = {}) {
    const params = new URLSearchParams({
        type: reportType,
        ...filters
    });
    return await apiCall(`/reports/custom?${params.toString()}`);
}

/**
 * Export report data
 * @param {string} reportType - Type of report
 * @param {string} format - 'csv', 'pdf', or 'excel'
 * @param {object} filters - Filter options
 * @returns {Promise} - Blob (file download)
 */
async function exportReport(reportType, format = 'pdf', filters = {}) {
    const params = new URLSearchParams({
        type: reportType,
        format: format,
        ...filters
    });
    return await apiCall(`/reports/export?${params.toString()}`);
}

/**
 * Get report filters configuration
 * @param {string} reportType - Type of report
 * @returns {Promise} - { filters: [...] }
 */
async function getReportFilters(reportType) {
    return await apiCall(`/reports/filters?type=${reportType}`);
}

/**
 * Get report preview data
 * @param {string} reportType - Type of report
 * @param {object} filters - Filter options
 * @returns {Promise} - { preview: [...] }
 */
async function getReportPreview(reportType, filters = {}) {
    const params = new URLSearchParams({
        type: reportType,
        ...filters
    });
    return await apiCall(`/reports/preview?${params.toString()}`);
}

/**
 * Schedule report generation
 * @param {object} data - Schedule data (type, filters, frequency, email)
 * @returns {Promise} - { scheduled: boolean, job_id: string }
 */
async function scheduleReport(data) {
    return await apiCall('/reports/schedule', 'POST', data);
}

/**
 * Get scheduled reports
 * @returns {Promise} - Array of scheduled report objects
 */
async function getScheduledReports() {
    return await apiCall('/reports/scheduled');
}

/**
 * Cancel scheduled report
 * @param {string} jobId - Scheduled job ID
 * @returns {Promise} - Success message
 */
async function cancelScheduledReport(jobId) {
    return await apiCall(`/reports/schedule/${jobId}`, 'DELETE');
}

// Export all functions for use in reports.html
window.ReportsAPI = {
    getEnrollmentReport,
    getAttendanceReport,
    getAssessmentReport,
    getRevenueReport,
    getCertificateReport,
    getInstructorReport,
    getCustomReport,
    exportReport,
    getReportFilters,
    getReportPreview,
    scheduleReport,
    getScheduledReports,
    cancelScheduledReport
};

console.log('📊 Reports API loaded successfully');
