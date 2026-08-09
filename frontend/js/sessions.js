/* ============================================
   STTIMS - Session Management JavaScript
   ============================================ */

// Sample Data
const batches = [
    { id: 1, name: 'Python Batch 1', courseId: 1 },
    { id: 2, name: 'Python Batch 2', courseId: 1 },
    { id: 3, name: 'Electrical Safety Weekend', courseId: 2 },
    { id: 4, name: 'Web Development PHP Batch 1', courseId: 3 }
];

const instructors = [
    { id: 1, name: 'Dr. Abebe Teshome' },
    { id: 2, name: 'Dr. Tigist Wolde' },
    { id: 3, name: 'Eng. Chalachew Assefa' },
    { id: 4, name: 'Ms. Kidist Tadesse' }
];

// Sample Sessions Data
let sessions = [
    {
        id: 1,
        code: 'S-2024-001',
        batchId: 1,
        instructorId: 1,
        sessionDate: '2024-02-01',
        startTime: '09:00',
        endTime: '12:00',
        topic: 'Introduction to Python',
        sessionType: 'Lecture',
        roomNumber: 'Room 101',
        status: 'Completed',
        notes: ''
    },
    {
        id: 2,
        code: 'S-2024-002',
        batchId: 1,
        instructorId: 1,
        sessionDate: '2024-02-03',
        startTime: '09:00',
        endTime: '12:00',
        topic: 'Python Syntax and Data Types',
        sessionType: 'Lecture',
        roomNumber: 'Room 101',
        status: 'Completed',
        notes: ''
    },
    {
        id: 3,
        code: 'S-2024-003',
        batchId: 1,
        instructorId: 1,
        sessionDate: '2024-02-05',
        startTime: '09:00',
        endTime: '12:00',
        topic: 'Control Structures',
        sessionType: 'Lecture',
        roomNumber: 'Room 101',
        status: 'Ongoing',
        notes: ''
    },
    {
        id: 4,
        code: 'S-2024-004',
        batchId: 3,
        instructorId: 2,
        sessionDate: '2024-02-17',
        startTime: '08:00',
        endTime: '13:00',
        topic: 'Introduction to Electrical Safety',
        sessionType: 'Lecture',
        roomNumber: 'Room 201',
        status: 'Scheduled',
        notes: ''
    },
    {
        id: 5,
        code: 'S-2024-005',
        batchId: 4,
        instructorId: 3,
        sessionDate: '2024-03-01',
        startTime: '14:00',
        endTime: '17:00',
        topic: 'PHP Basics',
        sessionType: 'Lecture',
        roomNumber: 'Room 103',
        status: 'Scheduled',
        notes: ''
    }
];

let filteredSessions = [...sessions];
let currentPage = 1;
const pageSize = 5;

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    populateSelects();
    renderTable();
    setupEventListeners();
});

// ============================================
// Setup Event Listeners
// ============================================
function setupEventListeners() {
    document.getElementById('saveSessionBtn').addEventListener('click', saveSession);
}

// ============================================
// Populate Selects
// ============================================
function populateSelects() {
    // Batches
    const batchSelects = ['sessionBatch', 'batchFilter'];
    batchSelects.forEach(id => {
        const select = document.getElementById(id);
        if (!select) return;
        
        select.innerHTML = id === 'batchFilter' 
            ? '<option value="">All Batches</option>'
            : '<option value="">Select Batch</option>';
        
        batches.forEach(batch => {
            const option = document.createElement('option');
            option.value = batch.id;
            option.textContent = batch.name;
            select.appendChild(option);
        });
    });
    
    // Instructors
    const instructorSelect = document.getElementById('sessionInstructor');
    if (instructorSelect) {
        instructorSelect.innerHTML = '<option value="">Select Instructor</option>';
        instructors.forEach(instructor => {
            const option = document.createElement('option');
            option.value = instructor.id;
            option.textContent = instructor.name;
            instructorSelect.appendChild(option);
        });
    }
}

// ============================================
// Render Table
// ============================================
function renderTable() {
    const tbody = document.getElementById('sessionsTableBody');
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageSessions = filteredSessions.slice(start, end);
    
    if (pageSessions.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center py-4 text-muted">
                    <i class="fas fa-clock fa-2x d-block mb-2"></i>
                    No sessions found
                </td>
            </tr>
        `;
        document.getElementById('sessionCount').textContent = '0';
        document.getElementById('tableInfo').textContent = 'Showing 0 of 0 sessions';
        return;
    }
    
    let html = '';
    pageSessions.forEach((session, index) => {
        const batch = batches.find(b => b.id === session.batchId);
        const instructor = instructors.find(i => i.id === session.instructorId);
        const statusBadge = getSessionStatusBadge(session.status);
        const typeBadge = getSessionTypeBadge(session.sessionType);
        
        html += `
            <tr>
                <td><span class="session-code">${session.code}</span></td>
                <td>${formatDate(session.sessionDate)}</td>
                <td><span class="session-time">${session.startTime} - ${session.endTime}</span></td>
                <td>
                    <span class="session-topic" title="${session.topic || 'N/A'}">
                        ${session.topic || 'N/A'}
                    </span>
                </td>
                <td>${instructor ? instructor.name : 'N/A'}</td>
                <td>${session.roomNumber || 'N/A'}</td>
                <td>${statusBadge}</td>
                <td>
                    <div class="d-flex gap-1">
                        <button class="btn btn-sm btn-outline-info" onclick="viewSession(${session.id})" title="View">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-primary" onclick="editSession(${session.id})" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-success" onclick="startSession(${session.id})" title="Start">
                            <i class="fas fa-play"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="cancelSession(${session.id})" title="Cancel">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
    document.getElementById('sessionCount').textContent = filteredSessions.length;
    document.getElementById('tableInfo').textContent = 
        `Showing ${start + 1} to ${Math.min(end, filteredSessions.length)} of ${filteredSessions.length} sessions`;
    
    renderPagination();
}

function renderPagination() {
    const totalPages = Math.ceil(filteredSessions.length / pageSize);
    const container = document.getElementById('paginationContainer');
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }
    
    let html = `
        <ul class="pagination pagination-sm mb-0">
            <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="goToPage(${currentPage - 1})">Previous</a>
            </li>
    `;
    for (let i = 1; i <= totalPages; i++) {
        html += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <a class="page-link" href="#" onclick="goToPage(${i})">${i}</a>
            </li>
        `;
    }
    html += `
            <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="goToPage(${currentPage + 1})">Next</a>
            </li>
        </ul>
    `;
    container.innerHTML = html;
}

function goToPage(page) {
    const totalPages = Math.ceil(filteredSessions.length / pageSize);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    renderTable();
}

// ============================================
// Filter and Search
// ============================================
function filterSessions() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const batchFilter = document.getElementById('batchFilter').value;
    const statusFilter = document.getElementById('statusFilter').value;
    
    filteredSessions = sessions.filter(session => {
        const matchSearch = (session.topic || '').toLowerCase().includes(search) || 
                           session.code.toLowerCase().includes(search);
        const matchBatch = !batchFilter || session.batchId === parseInt(batchFilter);
        const matchStatus = !statusFilter || session.status === statusFilter;
        return matchSearch && matchBatch && matchStatus;
    });
    
    currentPage = 1;
    renderTable();
}

function resetFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('batchFilter').value = '';
    document.getElementById('statusFilter').value = '';
    filteredSessions = [...sessions];
    currentPage = 1;
    renderTable();
}

function refreshTable() {
    filteredSessions = [...sessions];
    currentPage = 1;
    renderTable();
    showAlert('Table refreshed', 'success');
}

// ============================================
// Session Actions
// ============================================

function startSession(id) {
    const session = sessions.find(s => s.id === id);
    if (!session) return;
    
    if (session.status === 'Ongoing') {
        showAlert('Session is already ongoing', 'warning');
        return;
    }
    
    if (session.status === 'Completed') {
        showAlert('Cannot start a completed session', 'warning');
        return;
    }
    
    components.confirmAction(
        `Are you sure you want to start session "${session.code}"?`,
        function() {
            session.status = 'Ongoing';
            filteredSessions = [...sessions];
            renderTable();
            showAlert(`Session "${session.code}" started successfully`, 'success');
        }
    );
}

function cancelSession(id) {
    const session = sessions.find(s => s.id === id);
    if (!session) return;
    
    if (session.status === 'Cancelled') {
        showAlert('Session is already cancelled', 'warning');
        return;
    }
    
    if (session.status === 'Completed') {
        showAlert('Cannot cancel a completed session', 'warning');
        return;
    }
    
    components.confirmAction(
        `Are you sure you want to cancel session "${session.code}"?`,
        function() {
            session.status = 'Cancelled';
            filteredSessions = [...sessions];
            renderTable();
            showAlert(`Session "${session.code}" cancelled successfully`, 'success');
        }
    );
}

// ============================================
// CRUD Operations
// ============================================

function saveSession() {
    const form = document.getElementById('sessionForm');
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    const id = document.getElementById('editSessionId').value;
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    
    // Validate times
    if (startTime && endTime && startTime >= endTime) {
        showAlert('Start time must be before end time', 'danger');
        return;
    }
    
    const sessionData = {
        batchId: parseInt(document.getElementById('sessionBatch').value),
        instructorId: parseInt(document.getElementById('sessionInstructor').value),
        sessionDate: document.getElementById('sessionDate').value,
        startTime: startTime,
        endTime: endTime,
        topic: document.getElementById('sessionTopic').value.trim(),
        sessionType: document.getElementById('sessionType').value,
        roomNumber: document.getElementById('sessionRoom').value.trim(),
        status: document.getElementById('sessionStatus').value,
        notes: document.getElementById('sessionNotes').value.trim()
    };
    
    if (id) {
        const index = sessions.findIndex(s => s.id === parseInt(id));
        if (index !== -1) {
            sessions[index] = { ...sessions[index], ...sessionData };
            showAlert('Session updated successfully!', 'success');
        }
    } else {
        const newSession = {
            id: Math.max(...sessions.map(s => s.id), 0) + 1,
            code: `S-2024-${String(sessions.length + 1).padStart(3, '0')}`,
            ...sessionData
        };
        sessions.push(newSession);
        showAlert('Session created successfully!', 'success');
    }
    
    bootstrap.Modal.getInstance(document.getElementById('addSessionModal')).hide();
    filteredSessions = [...sessions];
    renderTable();
    resetSessionForm();
}

function editSession(id) {
    const session = sessions.find(s => s.id === id);
    if (!session) return;
    
    document.getElementById('editSessionId').value = session.id;
    document.getElementById('sessionModalTitle').textContent = 'Edit Session';
    document.getElementById('sessionBatch').value = session.batchId;
    document.getElementById('sessionInstructor').value = session.instructorId;
    document.getElementById('sessionDate').value = session.sessionDate;
    document.getElementById('startTime').value = session.startTime;
    document.getElementById('endTime').value = session.endTime;
    document.getElementById('sessionTopic').value = session.topic || '';
    document.getElementById('sessionType').value = session.sessionType;
    document.getElementById('sessionRoom').value = session.roomNumber || '';
    document.getElementById('sessionStatus').value = session.status;
    document.getElementById('sessionNotes').value = session.notes || '';
    
    const modal = new bootstrap.Modal(document.getElementById('addSessionModal'));
    modal.show();
}

function viewSession(id) {
    const session = sessions.find(s => s.id === id);
    if (!session) return;
    
    const body = document.getElementById('viewSessionBody');
    const batch = batches.find(b => b.id === session.batchId);
    const instructor = instructors.find(i => i.id === session.instructorId);
    const statusBadge = getSessionStatusBadge(session.status);
    const typeBadge = getSessionTypeBadge(session.sessionType);
    
    body.innerHTML = `
        <div class="row">
            <div class="col-md-10 mx-auto">
                <div class="text-center mb-3">
                    <span class="session-code" style="font-size: 1.2rem;">${session.code}</span>
                    <div class="mt-2">${statusBadge}</div>
                </div>
                <hr>
                <div class="row">
                    <div class="col-6">
                        <small class="text-muted d-block">Date</small>
                        <strong>${formatDate(session.sessionDate)}</strong>
                    </div>
                    <div class="col-6">
                        <small class="text-muted d-block">Time</small>
                        <strong>${session.startTime} - ${session.endTime}</strong>
                    </div>
                </div>
                <hr>
                <div class="row">
                    <div class="col-6">
                        <small class="text-muted d-block">Batch</small>
                        <strong>${batch ? batch.name : 'N/A'}</strong>
                    </div>
                    <div class="col-6">
                        <small class="text-muted d-block">Instructor</small>
                        <strong>${instructor ? instructor.name : 'N/A'}</strong>
                    </div>
                </div>
                <hr>
                <div class="row">
                    <div class="col-6">
                        <small class="text-muted d-block">Session Type</small>
                        ${typeBadge}
                    </div>
                    <div class="col-6">
                        <small class="text-muted d-block">Room</small>
                        <strong>${session.roomNumber || 'N/A'}</strong>
                    </div>
                </div>
                ${session.topic ? `
                <hr>
                <div class="row">
                    <div class="col-12">
                        <small class="text-muted d-block">Topic Covered</small>
                        <strong>${session.topic}</strong>
                    </div>
                </div>` : ''}
                ${session.notes ? `
                <hr>
                <div class="row">
                    <div class="col-12">
                        <small class="text-muted d-block">Notes</small>
                        <p>${session.notes}</p>
                    </div>
                </div>` : ''}
            </div>
        </div>
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('viewSessionModal'));
    modal.show();
}

function deleteSession(id) {
    const session = sessions.find(s => s.id === id);
    if (!session) return;
    
    components.confirmAction(
        `Are you sure you want to delete session "${session.code}"?`,
        function() {
            sessions = sessions.filter(s => s.id !== id);
            filteredSessions = [...sessions];
            renderTable();
            showAlert(`Session "${session.code}" deleted successfully`, 'success');
        }
    );
}

// ============================================
// Export Data
// ============================================
function exportData() {
    let csv = 'Code,Date,Time,Topic,Instructor,Room,Status\n';
    filteredSessions.forEach(s => {
        const batch = batches.find(b => b.id === s.batchId);
        const instructor = instructors.find(i => i.id === s.instructorId);
        csv += `${s.code},${s.sessionDate},${s.startTime}-${s.endTime},${s.topic || 'N/A'},${instructor ? instructor.name : 'N/A'},${s.roomNumber || 'N/A'},${s.status}\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `sessions_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// ============================================
// Reset Form
// ============================================
function resetSessionForm() {
    document.getElementById('sessionForm').reset();
    document.getElementById('sessionForm').classList.remove('was-validated');
    document.getElementById('editSessionId').value = '';
    document.getElementById('sessionModalTitle').textContent = 'Add New Session';
}

// ============================================
// Utility Functions
// ============================================
function getSessionStatusBadge(status) {
    const classes = {
        'Scheduled': 'badge-scheduled',
        'Ongoing': 'badge-ongoing',
        'Completed': 'badge-completed',
        'Cancelled': 'badge-cancelled'
    };
    const badgeClass = classes[status] || 'badge bg-secondary';
    return `<span class="badge ${badgeClass}">${status}</span>`;
}

function getSessionTypeBadge(type) {
    const classes = {
        'Lecture': 'lecture',
        'Lab': 'lab',
        'Workshop': 'workshop',
        'Practical': 'practical',
        'Review': 'review',
        'Exam': 'exam'
    };
    const cls = classes[type] || 'lecture';
    return `<span class="session-type-badge ${cls}">${type || 'N/A'}</span>`;
}

function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

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
    if (typeof sessions === 'undefined') {
        sessions = [];
    }
    filteredSessions = [...sessions];
    renderTable();
    populateSelects();
});
