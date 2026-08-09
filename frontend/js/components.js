/* ============================================
   STTIMS - Reusable Components
   ============================================ */

class Components {
    constructor() {
        this.init();
    }

    init() {
        this.initTableSort();
        this.initConfirmDialog();
    }

    // Table Sorting
    initTableSort() {
        const tables = document.querySelectorAll('.sortable-table');
        tables.forEach(table => {
            const headers = table.querySelectorAll('thead th');
            headers.forEach((header, index) => {
                if (!header.classList.contains('no-sort')) {
                    header.style.cursor = 'pointer';
                    header.addEventListener('click', () => this.sortTable(table, index));
                }
            });
        });
    }

    sortTable(table, columnIndex) {
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const isAsc = table.dataset.sortAsc === 'true';

        rows.sort((a, b) => {
            const aVal = a.children[columnIndex]?.textContent.trim() || '';
            const bVal = b.children[columnIndex]?.textContent.trim() || '';
            const aNum = parseFloat(aVal);
            const bNum = parseFloat(bVal);

            if (!isNaN(aNum) && !isNaN(bNum)) {
                return isAsc ? aNum - bNum : bNum - aNum;
            }
            return isAsc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        });

        rows.forEach(row => tbody.appendChild(row));
        table.dataset.sortAsc = !isAsc;
    }

    // Confirmation Dialog
    initConfirmDialog() {
        const confirmBtn = document.getElementById('confirmBtn');
        const modal = document.getElementById('confirmModal');

        if (confirmBtn && modal) {
            let callback = null;
            confirmBtn.addEventListener('click', () => {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) bsModal.hide();
                if (callback) {
                    callback();
                    callback = null;
                }
            });

            modal.addEventListener('hidden.bs.modal', () => {
                callback = null;
            });

            window._confirmCallback = (fn) => { callback = fn; };
        }
    }

    confirmAction(message, callback) {
        const modal = document.getElementById('confirmModal');
        const body = document.getElementById('confirmBody');
        if (!modal || !body) return;

        body.textContent = message;
        const bsModal = new bootstrap.Modal(modal);
        window._confirmCallback = callback;
        bsModal.show();
    }

    // Render Pagination
    renderPagination(containerId, currentPage, totalPages, onPageClick) {
        const container = document.getElementById(containerId);
        if (!container) return;

        let html = `
            <nav aria-label="Page navigation">
                <ul class="pagination justify-content-center">
                    <li class="page-item ${currentPage <= 1 ? 'disabled' : ''}">
                        <a class="page-link" href="#" data-page="${currentPage - 1}"><i class="fas fa-chevron-left"></i></a>
                    </li>
        `;

        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(totalPages, startPage + 4);

        if (startPage > 1) {
            html += `<li class="page-item"><a class="page-link" href="#" data-page="1">1</a></li>`;
            if (startPage > 2) html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
        }

        for (let i = startPage; i <= endPage; i++) {
            html += `<li class="page-item ${i === currentPage ? 'active' : ''}">
                <a class="page-link" href="#" data-page="${i}">${i}</a>
            </li>`;
        }

        if (endPage < totalPages) {
            if (endPage < totalPages - 1) html += `<li class="page-item disabled"><span class="page-link">...</span></li>`;
            html += `<li class="page-item"><a class="page-link" href="#" data-page="${totalPages}">${totalPages}</a></li>`;
        }

        html += `
                    <li class="page-item ${currentPage >= totalPages ? 'disabled' : ''}">
                        <a class="page-link" href="#" data-page="${currentPage + 1}"><i class="fas fa-chevron-right"></i></a>
                    </li>
                </ul>
            </nav>
        `;

        container.innerHTML = html;

        container.querySelectorAll('.page-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = parseInt(link.dataset.page);
                if (!isNaN(page) && onPageClick) {
                    onPageClick(page);
                }
            });
        });
    }

    // Loading Spinner
    showLoading(message = 'Loading...') {
        let overlay = document.getElementById('loadingOverlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loadingOverlay';
            overlay.className = 'loading-overlay';
            overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(255,255,255,0.8);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:9999;';
            overlay.innerHTML = `
                <div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>
                <p class="mt-2 text-muted">${message}</p>
            `;
            document.body.appendChild(overlay);
        } else {
            overlay.style.display = 'flex';
            const msg = overlay.querySelector('p');
            if (msg) msg.textContent = message;
        }
    }

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) overlay.style.display = 'none';
    }

    // Populate Table
    populateTable(tableId, data, columns) {
        const tbody = document.querySelector(`#${tableId} tbody`);
        if (!tbody) return;

        tbody.innerHTML = '';
        data.forEach((item, index) => {
            const row = document.createElement('tr');
            columns.forEach(col => {
                const td = document.createElement('td');
                if (typeof col === 'function') {
                    td.innerHTML = col(item, index);
                } else {
                    td.textContent = item[col] || '';
                }
                row.appendChild(td);
            });
            tbody.appendChild(row);
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.components = new Components();
});
