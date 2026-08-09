// dashboard-api.js
// Dashboard-specific API functions for STTIMS

/**
 * Get dashboard statistics
 * @returns {Promise} - { total_trainees, active_instructors, active_courses, 
 *                        certificates_issued, total_batches, active_enrollments,
 *                        upcoming_sessions, completion_rate, today_registrations,
 *                        pending_certificates, upcoming_deadlines, total_revenue,
 *                        pending_revenue }
 */
async function getDashboardStats() {
    return await apiCall('/dashboard/stats');
}

/**
 * Get recent activities
 * @param {number} limit - Number of activities to retrieve (default: 10)
 * @returns {Promise} - Array of activity objects with message, time_ago, icon, iconBg
 */
async function getDashboardActivities(limit = 10) {
    return await apiCall(`/dashboard/activities?limit=${limit}`);
}

/**
 * Get enrollment trends data
 * @param {string} period - '6m', '1y', or 'all' (default: '6m')
 * @returns {Promise} - { labels: [...], data: [...] }
 */
async function getEnrollmentTrends(period = '6m') {
    return await apiCall(`/dashboard/enrollment-trends?period=${period}`);
}

/**
 * Get revenue data
 * @returns {Promise} - { total_revenue, pending_revenue, paid_revenue, partial_revenue,
 *                        chart_data: { labels: [...], data: [...] } }
 */
async function getRevenueData() {
    return await apiCall('/dashboard/revenue');
}

/**
 * Get attendance summary
 * @returns {Promise} - { present: number, absent: number, late: number, 
 *                        percentage: number, total_records: number }
 */
async function getAttendanceSummary() {
    return await apiCall('/dashboard/attendance');
}

// Export all functions for use in dashboard.html
window.DashboardAPI = {
    getDashboardStats,
    getDashboardActivities,
    getEnrollmentTrends,
    getRevenueData,
    getAttendanceSummary
};

console.log('📊 Dashboard API loaded successfully');
