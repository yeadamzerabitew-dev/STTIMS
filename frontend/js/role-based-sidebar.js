// role-based-sidebar.js
// Role-based sidebar and access control

// Define role permissions
const ROLE_PERMISSIONS = {
    Admin: {
        menu: ['dashboard', 'users', 'trainees', 'instructors', 'categories', 'courses', 'batches', 'enrollments', 'attendance', 'assessments', 'results', 'certificates', 'reports', 'settings'],
        redirect: 'dashboard.html'
    },
    Manager: {
        menu: ['dashboard', 'trainees', 'instructors', 'categories', 'courses', 'batches', 'enrollments', 'reports', 'settings'],
        redirect: 'dashboard.html'
    },
    Instructor: {
        menu: ['dashboard', 'trainees', 'courses', 'batches', 'enrollments', 'attendance', 'assessments', 'results', 'certificates'],
        redirect: 'dashboard.html'
    },
    Trainee: {
        menu: ['dashboard', 'certificates', 'profile'],
        redirect: 'dashboard.html'
    }
};

// Menu item configuration
const MENU_ITEMS = {
    dashboard: { icon: 'fa-home', label: 'Dashboard', path: 'dashboard.html' },
    users: { icon: 'fa-users-cog', label: 'Users', path: 'users.html' },
    trainees: { icon: 'fa-user-graduate', label: 'Trainees', path: 'trainees.html' },
    instructors: { icon: 'fa-chalkboard-teacher', label: 'Instructors', path: 'instructors.html' },
    categories: { icon: 'fa-folder-open', label: 'Categories', path: 'categories.html' },
    courses: { icon: 'fa-book', label: 'Courses', path: 'courses.html' },
    batches: { icon: 'fa-layer-group', label: 'Batches', path: 'batches.html' },
    enrollments: { icon: 'fa-edit', label: 'Enrollments', path: 'enrollments.html' },
    attendance: { icon: 'fa-clipboard-check', label: 'Attendance', path: 'attendance.html' },
    assessments: { icon: 'fa-tasks', label: 'Assessments', path: 'assessments.html' },
    results: { icon: 'fa-chart-bar', label: 'Results', path: 'results.html' },
    certificates: { icon: 'fa-certificate', label: 'Certificates', path: 'certificates.html' },
    reports: { icon: 'fa-file-alt', label: 'Reports', path: 'reports.html' },
    settings: { icon: 'fa-cog', label: 'Settings', path: 'settings.html' },
    profile: { icon: 'fa-user', label: 'Profile', path: 'profile.html' }
};

/**
 * Get current user role
 */
function getUserRole() {
    try {
        const userData = localStorage.getItem('user') || sessionStorage.getItem('user');
        if (userData) {
            const user = JSON.parse(userData);
            return user.role || 'Trainee';
        }
    } catch (e) {
        console.error('Error getting user role:', e);
    }
    return 'Trainee';
}

/**
 * Get current user data
 */
function getUser() {
    try {
        const userData = localStorage.getItem('user') || sessionStorage.getItem('user');
        if (userData) {
            return JSON.parse(userData);
        }
    } catch (e) {
        console.error('Error getting user:', e);
    }
    return null;
}

/**
 * Check if user has access to a specific page
 */
function hasAccess(page) {
    const role = getUserRole();
    const permissions = ROLE_PERMISSIONS[role];
    if (!permissions) return false;
    return permissions.menu.includes(page);
}

/**
 * Generate sidebar based on user role
 */
function generateSidebar() {
    const role = getUserRole();
    const permissions = ROLE_PERMISSIONS[role];
    
    if (!permissions) {
        console.warn('No permissions found for role:', role);
        return '';
    }
    
    let html = '';
    
    // Generate menu items based on permissions
    for (const menuKey of permissions.menu) {
        const menuItem = MENU_ITEMS[menuKey];
        if (menuItem) {
            const isActive = window.location.pathname.includes(menuItem.path) ? 'active' : '';
            html += `
                <li class="nav-item">
                    <a class="nav-link ${isActive}" href="${menuItem.path}">
                        <i class="fas ${menuItem.icon}"></i>
                        <span>${menuItem.label}</span>
                    </a>
                </li>
            `;
        }
    }
    
    return html;
}

/**
 * Redirect if user doesn't have access to current page
 */
function checkPageAccess() {
    const currentPage = window.location.pathname.split('/').pop().replace('.html', '');
    
    // Check if current page is in the user's allowed menu
    const role = getUserRole();
    const permissions = ROLE_PERMISSIONS[role];
    
    if (!permissions) {
        window.location.href = 'login.html';
        return false;
    }
    
    // Special case: login page is always accessible
    if (currentPage === 'login' || currentPage === '') {
        return true;
    }
    
    // Check if page is in allowed menu
    const hasPageAccess = permissions.menu.includes(currentPage);
    
    if (!hasPageAccess) {
        console.warn(`Access denied for ${currentPage}. Redirecting to dashboard.`);
        window.location.href = permissions.redirect || 'dashboard.html';
        return false;
    }
    
    return true;
}

/**
 * Show/hide elements based on role
 */
function applyRoleBasedVisibility() {
    const role = getUserRole();
    const permissions = ROLE_PERMISSIONS[role];
    
    if (!permissions) return;
    
    // Hide elements with data-role attribute
    document.querySelectorAll('[data-role]').forEach(element => {
        const allowedRoles = element.dataset.role.split(',');
        if (!allowedRoles.includes(role)) {
            element.style.display = 'none';
        } else {
            element.style.display = '';
        }
    });
    
    // Show elements with data-role-hide
    document.querySelectorAll('[data-role-hide]').forEach(element => {
        const hiddenRoles = element.dataset.roleHide.split(',');
        if (hiddenRoles.includes(role)) {
            element.style.display = 'none';
        } else {
            element.style.display = '';
        }
    });
}

// Export functions
window.RoleBasedAccess = {
    getUserRole,
    getUser,
    hasAccess,
    generateSidebar,
    checkPageAccess,
    applyRoleBasedVisibility,
    ROLE_PERMISSIONS,
    MENU_ITEMS
};

console.log('🔐 Role-Based Access Control loaded');
console.log('👤 Current Role:', getUserRole());
