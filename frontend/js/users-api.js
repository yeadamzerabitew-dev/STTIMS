// users-api.js
// User-specific API functions for STTIMS

/**
 * Get list of users with pagination and filters
 * @param {number} page - Page number (default: 1)
 * @param {number} perPage - Items per page (default: 10)
 * @param {object} filters - Filter options (search, role, status)
 * @returns {Promise} - { data: [...], total: number, total_pages: number }
 */
async function getUsers(page = 1, perPage = 10, filters = {}) {
    const params = new URLSearchParams({
        page: page,
        per_page: perPage,
        ...filters
    });
    return await apiCall(`/users?${params.toString()}`);
}

/**
 * Get a single user by ID
 * @param {number} id - User ID
 * @returns {Promise} - User object
 */
async function getUser(id) {
    return await apiCall(`/users/${id}`);
}

/**
 * Create a new user
 * @param {object} data - User data (username, email, password, role, status)
 * @returns {Promise} - Created user object
 */
async function createUser(data) {
    return await apiCall('/users', 'POST', data);
}

/**
 * Update an existing user
 * @param {number} id - User ID
 * @param {object} data - Updated user data
 * @returns {Promise} - Updated user object
 */
async function updateUser(id, data) {
    return await apiCall(`/users/${id}`, 'PUT', data);
}

/**
 * Delete a user (soft delete)
 * @param {number} id - User ID
 * @returns {Promise} - Success message
 */
async function deleteUser(id) {
    return await apiCall(`/users/${id}`, 'DELETE');
}

/**
 * Reset user password
 * @param {number} id - User ID
 * @param {string} password - New password
 * @returns {Promise} - Success message
 */
async function resetUserPassword(id, password) {
    return await apiCall(`/users/${id}/reset-password`, 'POST', { password });
}

/**
 * Unlock a locked user account
 * @param {number} id - User ID
 * @returns {Promise} - Success message
 */
async function unlockUser(id) {
    return await apiCall(`/users/${id}/unlock`, 'POST');
}

/**
 * Get user profile
 * @param {number} id - User ID
 * @returns {Promise} - User profile object
 */
async function getUserProfile(id) {
    return await apiCall(`/users/${id}/profile`);
}

/**
 * Update user profile
 * @param {number} id - User ID
 * @param {object} data - Profile data
 * @returns {Promise} - Updated profile
 */
async function updateUserProfile(id, data) {
    return await apiCall(`/users/${id}/profile`, 'PUT', data);
}

/**
 * Get user activity log
 * @param {number} id - User ID
 * @param {number} limit - Number of logs to retrieve (default: 20)
 * @returns {Promise} - Array of log entries
 */
async function getUserActivityLog(id, limit = 20) {
    return await apiCall(`/users/${id}/activity?limit=${limit}`);
}

/**
 * Get user permissions
 * @param {number} id - User ID
 * @returns {Promise} - Array of permissions
 */
async function getUserPermissions(id) {
    return await apiCall(`/users/${id}/permissions`);
}

/**
 * Update user permissions
 * @param {number} id - User ID
 * @param {array} permissions - Array of permission strings
 * @returns {Promise} - Updated permissions
 */
async function updateUserPermissions(id, permissions) {
    return await apiCall(`/users/${id}/permissions`, 'PUT', { permissions });
}

/**
 * Check if username is available
 * @param {string} username - Username to check
 * @returns {Promise} - { available: boolean }
 */
async function checkUsernameAvailability(username) {
    return await apiCall(`/users/check-username?username=${encodeURIComponent(username)}`);
}

/**
 * Check if email is available
 * @param {string} email - Email to check
 * @returns {Promise} - { available: boolean }
 */
async function checkEmailAvailability(email) {
    return await apiCall(`/users/check-email?email=${encodeURIComponent(email)}`);
}

// Export all functions for use in users.html
window.UsersAPI = {
    getUsers,
    getUser,
    createUser,
    updateUser,
    deleteUser,
    resetUserPassword,
    unlockUser,
    getUserProfile,
    updateUserProfile,
    getUserActivityLog,
    getUserPermissions,
    updateUserPermissions,
    checkUsernameAvailability,
    checkEmailAvailability
};

console.log('👥 Users API loaded successfully');
