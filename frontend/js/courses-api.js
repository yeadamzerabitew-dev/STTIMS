// courses-api.js
// Course-specific API functions for STTIMS

/**
 * Get list of courses with pagination and filters
 * @param {number} page - Page number (default: 1)
 * @param {number} perPage - Items per page (default: 10)
 * @param {object} filters - Filter options (search, category_id, course_level, status)
 * @returns {Promise} - { data: [...], total: number, total_pages: number }
 */
async function getCourses(page = 1, perPage = 10, filters = {}) {
    const params = new URLSearchParams({
        page: page,
        per_page: perPage,
        ...filters
    });
    return await apiCall(`/courses?${params.toString()}`);
}

/**
 * Get a single course by ID
 * @param {number} id - Course ID
 * @returns {Promise} - Course object
 */
async function getCourse(id) {
    return await apiCall(`/courses/${id}`);
}

/**
 * Create a new course
 * @param {object} data - Course data (course_code, course_title, category_id, etc.)
 * @returns {Promise} - Created course object
 */
async function createCourse(data) {
    return await apiCall('/courses', 'POST', data);
}

/**
 * Update an existing course
 * @param {number} id - Course ID
 * @param {object} data - Updated course data
 * @returns {Promise} - Updated course object
 */
async function updateCourse(id, data) {
    return await apiCall(`/courses/${id}`, 'PUT', data);
}

/**
 * Delete a course (soft delete)
 * @param {number} id - Course ID
 * @returns {Promise} - Success message
 */
async function deleteCourse(id) {
    return await apiCall(`/courses/${id}`, 'DELETE');
}

/**
 * Search for courses by keyword
 * @param {string} query - Search query (title or code)
 * @returns {Promise} - Array of matching courses
 */
async function searchCourses(query) {
    return await apiCall(`/courses/search?q=${encodeURIComponent(query)}`);
}

/**
 * Get all batches for a course
 * @param {number} id - Course ID
 * @returns {Promise} - Array of batch objects
 */
async function getCourseBatches(id) {
    return await apiCall(`/courses/${id}/batches`);
}

/**
 * Get enrollment statistics for a course
 * @param {number} id - Course ID
 * @returns {Promise} - { total_enrollments, active_enrollments, completed, dropped }
 */
async function getCourseEnrollments(id) {
    return await apiCall(`/courses/${id}/enrollments`);
}

/**
 * Get course statistics
 * @param {number} id - Course ID
 * @returns {Promise} - { total_batches, total_trainees, completion_rate, avg_score }
 */
async function getCourseStatistics(id) {
    return await apiCall(`/courses/${id}/statistics`);
}

/**
 * Toggle course status
 * @param {number} id - Course ID
 * @param {string} status - 'Active', 'Inactive', or 'Archived'
 * @returns {Promise} - Updated course object
 */
async function toggleCourseStatus(id, status) {
    return await apiCall(`/courses/${id}/status`, 'PATCH', { status });
}

/**
 * Export courses data
 * @param {string} format - 'csv' or 'pdf' (default: 'csv')
 * @param {object} filters - Filter options
 * @returns {Promise} - Blob (file download)
 */
async function exportCourses(format = 'csv', filters = {}) {
    const params = new URLSearchParams({
        format: format,
        ...filters
    });
    return await apiCall(`/courses/export?${params.toString()}`);
}

/**
 * Get course categories
 * @returns {Promise} - Array of category objects
 */
async function getCourseCategories() {
    return await apiCall('/courses/categories');
}

/**
 * Get popular courses (most enrolled)
 * @param {number} limit - Number of courses to retrieve (default: 5)
 * @returns {Promise} - Array of course objects with enrollment count
 */
async function getPopularCourses(limit = 5) {
    return await apiCall(`/courses/popular?limit=${limit}`);
}

/**
 * Get course availability
 * @param {number} id - Course ID
 * @returns {Promise} - { available: boolean, next_batch_date: string }
 */
async function getCourseAvailability(id) {
    return await apiCall(`/courses/${id}/availability`);
}

/**
 * Bulk import courses
 * @param {File} file - CSV or Excel file
 * @returns {Promise} - { imported: number, failed: number, errors: [...] }
 */
async function importCourses(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const token = localStorage.getItem('authToken');
    const response = await fetch(`${API_BASE_URL}/courses/import`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        },
        body: formData
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || 'Failed to import courses');
    }
    
    return await response.json();
}

/**
 * Get course prerequisites
 * @param {number} id - Course ID
 * @returns {Promise} - Array of prerequisite courses
 */
async function getCoursePrerequisites(id) {
    return await apiCall(`/courses/${id}/prerequisites`);
}

// Export all functions for use in courses.html
window.CoursesAPI = {
    getCourses,
    getCourse,
    createCourse,
    updateCourse,
    deleteCourse,
    searchCourses,
    getCourseBatches,
    getCourseEnrollments,
    getCourseStatistics,
    toggleCourseStatus,
    exportCourses,
    getCourseCategories,
    getPopularCourses,
    getCourseAvailability,
    importCourses,
    getCoursePrerequisites
};

console.log('📚 Courses API loaded successfully');
