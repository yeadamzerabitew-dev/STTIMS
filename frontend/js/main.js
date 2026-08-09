/* ============================================
   STTIMS - Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebarToggle');
    const closeBtn = document.getElementById('sidebarClose');
    const overlay = document.querySelector('.sidebar-overlay');

    function toggleSidebar() {
        sidebar.classList.toggle('show');
        if (overlay) overlay.classList.toggle('show');
    }

    function closeSidebar() {
        sidebar.classList.remove('show');
        if (overlay) overlay.classList.remove('show');
    }

    if (toggleBtn) toggleBtn.addEventListener('click', toggleSidebar);
    if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
    if (overlay) overlay.addEventListener('click', closeSidebar);

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('show')) {
            closeSidebar();
        }
    });

    window.addEventListener('resize', function() {
        if (window.innerWidth >= 992 && sidebar.classList.contains('show')) {
            closeSidebar();
        }
    });

    // Active Navigation Link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href.split('/').pop())) {
            link.classList.add('active');
        }
    });
});

// Utility Functions
function formatCurrency(amount, currency = 'ETB') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function formatDate(date) {
    if (!date) return 'N/A';
    const d = new Date(date);
    return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatDateTime(date) {
    if (!date) return 'N/A';
    const d = new Date(date);
    return d.toLocaleString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit'
    });
}

function getStatusBadge(status) {
    const classes = {
        'Active': 'badge-active',
        'Inactive': 'badge-inactive',
        'Pending': 'badge-pending',
        'Completed': 'badge-completed',
        'Paid': 'badge-active',
        'Ongoing': 'badge-completed',
        'Upcoming': 'badge-pending',
        'Cancelled': 'badge-inactive'
    };
    const badgeClass = classes[status] || 'badge bg-secondary';
    return `<span class="badge ${badgeClass}">${status}</span>`;
}

function getInitials(firstName, lastName) {
    if (!firstName && !lastName) return 'U';
    return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase();
}

function debounce(func, wait = 300) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

// Toast Notifications
function showToast(message, type = 'info', duration = 5000) {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        container.style.cssText = 'position:fixed;top:70px;right:20px;z-index:9999;min-width:300px;';
        document.body.appendChild(container);
    }

    const icons = { success: 'fa-check-circle', danger: 'fa-exclamation-circle', warning: 'fa-exclamation-triangle', info: 'fa-info-circle' };
    const colors = { success: '#10B981', danger: '#EF4444', warning: '#F59E0B', info: '#3B82F6' };

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0 fade show`;
    toast.role = 'alert';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas ${icons[type] || icons.info} me-2"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, duration);
}
/* ============================================
   STTIMS - Responsive JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // SIDEBAR TOGGLE FOR MOBILE
    // ============================================
    
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarClose = document.getElementById('sidebarClose');
    const overlay = document.querySelector('.sidebar-overlay');
    
    // Create overlay if it doesn't exist
    if (!overlay) {
        const newOverlay = document.createElement('div');
        newOverlay.className = 'sidebar-overlay';
        document.body.appendChild(newOverlay);
    }
    
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    
    function toggleSidebar() {
        sidebar.classList.toggle('show');
        if (sidebarOverlay) {
            sidebarOverlay.classList.toggle('show');
        }
        document.body.classList.toggle('sidebar-open');
    }
    
    function closeSidebar() {
        sidebar.classList.remove('show');
        if (sidebarOverlay) {
            sidebarOverlay.classList.remove('show');
        }
        document.body.classList.remove('sidebar-open');
    }
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    
    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }
    
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }
    
    // Close sidebar on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar.classList.contains('show')) {
            closeSidebar();
        }
    });
    
    // Auto-close sidebar on window resize to desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 992 && sidebar.classList.contains('show')) {
            closeSidebar();
        }
    });
    
    // ============================================
    // RESPONSIVE TABLE - CARD VIEW ON MOBILE
    // ============================================
    
    function applyCardViewToTables() {
        const tables = document.querySelectorAll('.table-card-view');
        const isMobile = window.innerWidth <= 575.98;
        
        tables.forEach(table => {
            const thead = table.querySelector('thead');
            const tbody = table.querySelector('tbody');
            
            if (isMobile && thead) {
                thead.style.display = 'none';
                
                // Add data-label attributes to each cell
                const headers = thead.querySelectorAll('th');
                const rows = tbody.querySelectorAll('tr');
                
                rows.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    cells.forEach((cell, index) => {
                        if (headers[index]) {
                            cell.setAttribute('data-label', headers[index].textContent.trim());
                        }
                    });
                });
            } else if (!isMobile && thead) {
                thead.style.display = '';
            }
        });
    }
    
    // Apply on load and resize
    applyCardViewToTables();
    window.addEventListener('resize', applyCardViewToTables);
    
    // ============================================
    // RESPONSIVE CHART RESIZE
    // ============================================
    
    if (window.Chart) {
        // Store chart instances for resizing
        window.chartInstances = window.chartInstances || [];
        
        // Resize charts on window resize
        let resizeTimeout;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(function() {
                window.chartInstances.forEach(chart => {
                    if (chart && chart.resize) {
                        chart.resize();
                    }
                });
            }, 200);
        });
    }
    
    // ============================================
    // TOUCH DEVICE OPTIMIZATION
    // ============================================
    
    // Detect touch device
    if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
        document.body.classList.add('touch-device');
    }
    
    // ============================================
    // VIEWPORT HEIGHT FIX FOR MOBILE
    // ============================================
    
    function setVH() {
        let vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', vh + 'px');
    }
    
    setVH();
    window.addEventListener('resize', setVH);
    
    // ============================================
    // DROPDOWN RESPONSIVE BEHAVIOR
    // ============================================
    
    // Close dropdowns when clicking outside on mobile
    document.addEventListener('click', function(e) {
        const dropdowns = document.querySelectorAll('.dropdown-menu');
        dropdowns.forEach(dropdown => {
            if (!dropdown.parentElement.contains(e.target)) {
                // Close dropdown logic handled by Bootstrap
            }
        });
    });
});
