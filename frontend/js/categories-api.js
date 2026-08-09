// categories-api.js
// Category-specific API functions for STTIMS

/**
 * Get list of categories with filters
 * @param {object} filters - Filter options (search, status)
 * @returns {Promise} - Array of category objects
 */
async function getCategories(filters = {}) {
    const params = new URLSearchParams(filters);
    return await apiCall(`/categories?${params.toString()}`);
}

/**
 * Get a single category by ID
 * @param {number} id - Category ID
 * @returns {Promise} - Category object
 */
async function getCategory(id) {
    return await apiCall(`/categories/${id}`);
}

/**
 * Create a new category
 * @param {object} data - Category data (category_name, category_code, parent_category_id, description, display_order, status)
 * @returns {Promise} - Created category object
 */
async function createCategory(data) {
    return await apiCall('/categories', 'POST', data);
}

/**
 * Update an existing category
 * @param {number} id - Category ID
 * @param {object} data - Updated category data
 * @returns {Promise} - Updated category object
 */
async function updateCategory(id, data) {
    return await apiCall(`/categories/${id}`, 'PUT', data);
}

/**
 * Delete a category
 * @param {number} id - Category ID
 * @returns {Promise} - Success message
 */
async function deleteCategory(id) {
    return await apiCall(`/categories/${id}`, 'DELETE');
}

/**
 * Get category hierarchy tree
 * @returns {Promise} - Nested category tree structure
 */
async function getCategoryTree() {
    return await apiCall('/categories/tree');
}

/**
 * Get all courses in a category
 * @param {number} id - Category ID
 * @returns {Promise} - Array of course objects
 */
async function getCategoryCourses(id) {
    return await apiCall(`/categories/${id}/courses`);
}

/**
 * Get category statistics
 * @param {number} id - Category ID
 * @returns {Promise} - { total_courses, active_courses, total_batches, total_enrollments }
 */
async function getCategoryStatistics(id) {
    return await apiCall(`/categories/${id}/statistics`);
}

/**
 * Get subcategories of a category
 * @param {number} id - Category ID
 * @returns {Promise} - Array of subcategory objects
 */
async function getSubcategories(id) {
    return await apiCall(`/categories/${id}/subcategories`);
}

/**
 * Bulk update category display order
 * @param {array} categories - Array of { category_id, display_order }
 * @returns {Promise} - Success message
 */
async function updateCategoryOrder(categories) {
    return await apiCall('/categories/reorder', 'PUT', { categories });
}

/**
 * Toggle category status
 * @param {number} id - Category ID
 * @param {string} status - 'Active' or 'Inactive'
 * @returns {Promise} - Updated category object
 */
async function toggleCategoryStatus(id, status) {
    return await apiCall(`/categories/${id}/status`, 'PATCH', { status });
}

// Export all functions for use in categories.html
window.CategoriesAPI = {
    getCategories,
    getCategory,
    createCategory,
    updateCategory,
    deleteCategory,
    getCategoryTree,
    getCategoryCourses,
    getCategoryStatistics,
    getSubcategories,
    updateCategoryOrder,
    toggleCategoryStatus
};

console.log('📁 Categories API loaded successfully');
