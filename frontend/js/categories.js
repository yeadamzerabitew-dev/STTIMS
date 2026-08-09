/* ============================================
   STTIMS - Category Management JavaScript
   ============================================ */

// Sample Categories Data
let categories = [
    {
        id: 1,
        name: 'Information Technology',
        code: 'IT',
        description: 'Computer and Information Technology courses',
        parentId: null,
        displayOrder: 1,
        status: 'Active'
    },
    {
        id: 2,
        name: 'Programming',
        code: 'PROG',
        description: 'Programming and Software Development',
        parentId: 1,
        displayOrder: 1,
        status: 'Active'
    },
    {
        id: 3,
        name: 'Networking',
        code: 'NET',
        description: 'Network Administration and Security',
        parentId: 1,
        displayOrder: 2,
        status: 'Active'
    },
    {
        id: 4,
        name: 'Electrical Engineering',
        code: 'EE',
        description: 'Electrical and Electronics Engineering',
        parentId: null,
        displayOrder: 2,
        status: 'Active'
    },
    {
        id: 5,
        name: 'Power Systems',
        code: 'PWR',
        description: 'Power Systems Analysis and Design',
        parentId: 4,
        displayOrder: 1,
        status: 'Active'
    },
    {
        id: 6,
        name: 'Electronics',
        code: 'ELEC',
        description: 'Electronics and Circuit Design',
        parentId: 4,
        displayOrder: 2,
        status: 'Active'
    },
    {
        id: 7,
        name: 'Software Engineering',
        code: 'SE',
        description: 'Software Development and Engineering',
        parentId: null,
        displayOrder: 3,
        status: 'Active'
    },
    {
        id: 8,
        name: 'Web Development',
        code: 'WEB',
        description: 'Web Development Technologies',
        parentId: 7,
        displayOrder: 1,
        status: 'Active'
    },
    {
        id: 9,
        name: 'Database Management',
        code: 'DB',
        description: 'Database Design and Administration',
        parentId: 7,
        displayOrder: 2,
        status: 'Inactive'
    }
];

let filteredCategories = [...categories];
let currentAction = null;
let currentCategoryId = null;

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    renderCategoryTree();
    setupEventListeners();
    populateParentSelect();
});

// ============================================
// Setup Event Listeners
// ============================================
function setupEventListeners() {
    document.getElementById('saveCategoryBtn').addEventListener('click', saveCategory);
}

// ============================================
// Populate Parent Select
// ============================================
function populateParentSelect(excludeId = null) {
    const select = document.getElementById('parentCategory');
    const currentValue = select.value;
    
    select.innerHTML = '<option value="">None (Root Category)</option>';
    
    // Get root categories
    const rootCategories = categories.filter(c => c.parentId === null && c.id !== excludeId);
    rootCategories.sort((a, b) => a.displayOrder - b.displayOrder);
    
    rootCategories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.id;
        option.textContent = cat.name;
        select.appendChild(option);
        
        // Add children
        addChildrenToSelect(select, cat.id, 1, excludeId);
    });
    
    // Restore selected value if it exists
    if (currentValue && !excludeId) {
        select.value = currentValue;
    }
}

function addChildrenToSelect(select, parentId, level, excludeId) {
    const children = categories.filter(c => c.parentId === parentId && c.id !== excludeId);
    children.sort((a, b) => a.displayOrder - b.displayOrder);
    
    children.forEach(child => {
        const option = document.createElement('option');
        option.value = child.id;
        option.textContent = '— '.repeat(level) + child.name;
        select.appendChild(option);
        addChildrenToSelect(select, child.id, level + 1, excludeId);
    });
}

// ============================================
// Render Category Tree
// ============================================
function renderCategoryTree() {
    const container = document.getElementById('categoryTree');
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;
    
    // Apply filters
    let displayCategories = categories;
    if (searchTerm) {
        displayCategories = displayCategories.filter(c => 
            c.name.toLowerCase().includes(searchTerm) || 
            c.code.toLowerCase().includes(searchTerm)
        );
    }
    if (statusFilter) {
        displayCategories = displayCategories.filter(c => c.status === statusFilter);
    }
    
    // Get root categories
    const rootCategories = displayCategories.filter(c => c.parentId === null);
    rootCategories.sort((a, b) => a.displayOrder - b.displayOrder);
    
    document.getElementById('categoryCount').textContent = categories.length;
    
    if (rootCategories.length === 0) {
        container.innerHTML = `
            <div class="text-center py-4 text-muted">
                <i class="fas fa-folder-open fa-3x d-block mb-2"></i>
                <p>No categories found. Add your first category!</p>
            </div>
        `;
        return;
    }
    
    let html = '<ul class="category-tree">';
    rootCategories.forEach(cat => {
        html += buildCategoryTreeHTML(cat, displayCategories, 0);
    });
    html += '</ul>';
    
    container.innerHTML = html;
}

function buildCategoryTreeHTML(category, displayCategories, level) {
    const children = displayCategories.filter(c => c.parentId === category.id);
    children.sort((a, b) => a.displayOrder - b.displayOrder);
    
    const hasChildren = children.length > 0;
    const statusBadge = category.status === 'Active' 
        ? '<span class="badge badge-active">Active</span>'
        : '<span class="badge badge-inactive">Inactive</span>';
    
    let html = `<li class="level-${level}">`;
    html += `
        <div class="category-item">
            <div class="d-flex align-items-center">
                ${hasChildren ? `<span class="subcategory-toggle" onclick="toggleSubcategories(this)"><i class="fas fa-chevron-right"></i></span>` : '<span style="width:24px;"></span>'}
                <i class="fas fa-folder me-2 text-primary"></i>
                <span class="category-name">${category.name}</span>
                <span class="category-code">(${category.code})</span>
                <span class="ms-2">${statusBadge}</span>
                ${category.description ? `<small class="text-muted ms-2">- ${category.description}</small>` : ''}
            </div>
            <div class="category-actions">
                <button class="btn btn-sm btn-outline-primary" onclick="editCategory(${category.id})" title="Edit">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteCategory(${category.id})" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    
    if (hasChildren) {
        html += `<ul class="subcategories" style="display: none;">`;
        children.forEach(child => {
            html += buildCategoryTreeHTML(child, displayCategories, level + 1);
        });
        html += `</ul>`;
    }
    
    html += `</li>`;
    return html;
}

function toggleSubcategories(element) {
    const parent = element.closest('.category-item').parentElement;
    const subcategories = parent.querySelector('.subcategories');
    if (subcategories) {
        if (subcategories.style.display === 'none') {
            subcategories.style.display = 'block';
            element.classList.add('open');
        } else {
            subcategories.style.display = 'none';
            element.classList.remove('open');
        }
    }
}

// ============================================
// Filter Functions
// ============================================
function filterCategories() {
    renderCategoryTree();
}

function resetFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('statusFilter').value = '';
    renderCategoryTree();
}

function refreshTree() {
    renderCategoryTree();
    showAlert('Category tree refreshed', 'success');
}

// ============================================
// CRUD Operations
// ============================================

function saveCategory() {
    const form = document.getElementById('categoryForm');
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    const id = document.getElementById('editCategoryId').value;
    const name = document.getElementById('categoryName').value.trim();
    const code = document.getElementById('categoryCode').value.trim().toUpperCase();
    const parentId = document.getElementById('parentCategory').value;
    const description = document.getElementById('categoryDescription').value.trim();
    const displayOrder = parseInt(document.getElementById('displayOrder').value) || 0;
    const status = document.getElementById('categoryStatus').value;
    
    // Validate code uniqueness
    const existingCode = categories.find(c => c.code === code && c.id !== parseInt(id));
    if (existingCode) {
        showAlert('Category code already exists. Please use a different code.', 'danger');
        return;
    }
    
    // Validate name uniqueness
    const existingName = categories.find(c => c.name === name && c.id !== parseInt(id));
    if (existingName) {
        showAlert('Category name already exists. Please use a different name.', 'danger');
        return;
    }
    
    // Prevent self-parenting
    if (parentId && parseInt(parentId) === parseInt(id)) {
        showAlert('Cannot set a category as its own parent.', 'danger');
        return;
    }
    
    const categoryData = {
        name,
        code,
        parentId: parentId ? parseInt(parentId) : null,
        description,
        displayOrder,
        status
    };
    
    if (id) {
        // Edit existing category
        const index = categories.findIndex(c => c.id === parseInt(id));
        if (index !== -1) {
            // Check if moving category under its own child
            if (parentId) {
                const isChild = isCategoryChild(parseInt(id), parseInt(parentId));
                if (isChild) {
                    showAlert('Cannot move a category under its own child.', 'danger');
                    return;
                }
            }
            categories[index] = { ...categories[index], ...categoryData };
            showAlert('Category updated successfully!', 'success');
        }
    } else {
        // Add new category
        const newCategory = {
            id: Math.max(...categories.map(c => c.id), 0) + 1,
            ...categoryData
        };
        categories.push(newCategory);
        showAlert('Category created successfully!', 'success');
    }
    
    bootstrap.Modal.getInstance(document.getElementById('addCategoryModal')).hide();
    renderCategoryTree();
    resetCategoryForm();
    populateParentSelect();
}

function isCategoryChild(parentId, childId) {
    const children = categories.filter(c => c.parentId === parentId);
    for (const child of children) {
        if (child.id === childId) return true;
        if (isCategoryChild(child.id, childId)) return true;
    }
    return false;
}

function editCategory(id) {
    const category = categories.find(c => c.id === id);
    if (!category) return;
    
    document.getElementById('editCategoryId').value = category.id;
    document.getElementById('categoryModalTitle').textContent = 'Edit Category';
    document.getElementById('categoryName').value = category.name;
    document.getElementById('categoryCode').value = category.code;
    document.getElementById('categoryDescription').value = category.description || '';
    document.getElementById('displayOrder').value = category.displayOrder || 0;
    document.getElementById('categoryStatus').value = category.status;
    
    // Populate parent select excluding current category
    populateParentSelect(id);
    if (category.parentId) {
        document.getElementById('parentCategory').value = category.parentId;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('addCategoryModal'));
    modal.show();
}

function deleteCategory(id) {
    const category = categories.find(c => c.id === id);
    if (!category) return;
    
    // Check if category has children
    const hasChildren = categories.some(c => c.parentId === id);
    if (hasChildren) {
        showAlert('Cannot delete a category that has subcategories. Delete or move subcategories first.', 'danger');
        return;
    }
    
    components.confirmAction(
        `Are you sure you want to delete category "${category.name}"?`,
        function() {
            categories = categories.filter(c => c.id !== id);
            renderCategoryTree();
            populateParentSelect();
            showAlert(`Category "${category.name}" deleted successfully`, 'success');
        }
    );
}

// ============================================
// Reset Form
// ============================================
function resetCategoryForm() {
    document.getElementById('categoryForm').reset();
    document.getElementById('categoryForm').classList.remove('was-validated');
    document.getElementById('editCategoryId').value = '';
    document.getElementById('categoryModalTitle').textContent = 'Add New Category';
    document.getElementById('displayOrder').value = 0;
    populateParentSelect();
}

// ============================================
// Utility Functions
// ============================================
function showAlert(message, type = 'info') {
    const container = document.getElementById('alertContainer');
    const icons = {
        success: 'fa-check-circle',
        danger: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            <i class="fas ${icons[type] || icons.info} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    setTimeout(() => {
        const alert = container.querySelector('.alert');
        if (alert) {
            alert.classList.remove('show');
            setTimeout(() => container.innerHTML = '', 300);
        }
    }, 5000);
}

// ============================================
// Initialize on page load
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    if (typeof categories === 'undefined') {
        categories = [];
    }
    filteredCategories = [...categories];
    renderCategoryTree();
    populateParentSelect();
});
