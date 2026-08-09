// apply-role-guard.js
// Include this AFTER role-based-sidebar.js on every authenticated page.
// It redirects users who land on a page their role can't access, and
// replaces the page's static sidebar menu with the role-filtered one.

document.addEventListener('DOMContentLoaded', function () {
    if (typeof RoleBasedAccess === 'undefined') {
        console.warn('apply-role-guard.js: role-based-sidebar.js not loaded');
        return;
    }

    // Redirect away if this role isn't allowed on this page at all
    RoleBasedAccess.checkPageAccess();

    // Replace the sidebar's menu items with the role-filtered set
    const sidebarMenu = document.querySelector('#sidebar ul.nav.flex-column');
    if (sidebarMenu) {
        sidebarMenu.innerHTML = RoleBasedAccess.generateSidebar();
    }

    // Hide/show any elements tagged with data-role="Admin,Manager" etc.
    RoleBasedAccess.applyRoleBasedVisibility();
});
