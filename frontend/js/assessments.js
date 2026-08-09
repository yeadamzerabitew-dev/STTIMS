/* ============================================
   STTIMS - Assessment Management JavaScript
   ============================================ */

// Sample Data
const batches = [
    { id: 1, name: 'Python Batch 1', courseId: 1 },
    { id: 2, name: 'Python Batch 2', courseId: 1 },
    { id: 3, name: 'Electrical Safety Weekend', courseId: 2 },
    { id: 4, name: 'Web Development PHP Batch 1', courseId: 3 }
];

// Sample Assessments Data
let assessments = [
    {
        id: 1,
        code: 'A-2024-001',
        title: 'Python Basics Quiz',
        type: 'Quiz',
        batchId: 1,
        maxMarks: 20,
        weightage: 20,
        passingMarks: 10,
        date: '2024-02-15',
        startTime: '09:00',
        endTime: '09:30',
        duration: 30,
        totalQuestions: 10,
        description: 'Basic Python concepts and syntax',
        instructions: 'Answer all multiple choice questions',
        status: 'Completed',
        notes: ''
    },
    {
        id: 2,
        code: 'A-2024-002',
        title: 'Python Midterm Exam',
        type: 'Exam',
        batchId: 1,
        maxMarks: 50,
        weightage: 30,
        passingMarks: 25,
        date: '2024-03-01',
        startTime: '09:00',
        endTime: '11:00',
        duration: 120,
        totalQuestions: 15,
        description: 'Comprehensive test on Python',
        instructions: 'Choose the best answer and write code',
        status: 'Scheduled',
        notes: ''
    },
    {
        id: 3,
        code: 'A-2024-003',
        title: 'Python Final Project',
        type: 'Project',
        batchId: 1,
        maxMarks: 100,
        weightage: 40,
        passingMarks: 50,
        date: '2024-03-25',
        startTime: '09:00',
        endTime: '17:00',
        duration: 480,
        totalQuestions: null,
        description: 'Build a complete Python application',
        instructions: 'Submit your code with documentation',
        status: 'Scheduled',
        notes: ''
    },
    {
        id: 4,
        code: 'A-2024-004',
        title: 'Safety Standards Quiz',
        type: 'Quiz',
        batchId: 3,
        maxMarks: 20,
        weightage: 20,
        passingMarks: 10,
        date: '2024-03-05',
        startTime: '10:00',
        endTime: '10:30',
        duration: 30,
        totalQuestions: 10,
        description: 'Safety regulations and standards',
        instructions: 'Multiple choice questions',
        status: 'Completed',
        notes: ''
    },
    {
        id: 5,
        code: 'A-2024-005',
        title: 'Project Management Midterm',
        type: 'Exam',
        batchId: 4,
        maxMarks: 50,
        weightage: 30,
        passingMarks: 25,
        date: '2024-03-20',
        startTime: '10:00',
        endTime: '12:00',
        duration: 120,
        totalQuestions: 15,
        description: 'Project management fundamentals',
        instructions: 'Case study analysis',
        status: 'Scheduled',
        notes: ''
    }
];

let filteredAssessments = [...assessments];
let currentPage = 1;
const pageSize = 5;

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    populateBatchSelect();
    renderTable();
    setupEventListeners();
    setupWeightageListener();
});

// ============================================
// Setup Event Listeners
// ============================================
function setupEventListeners() {
    document.getElementById('saveAssessmentBtn').addEventListener('click', saveAssessment);
}

function setupWeightageListener() {
    document.getElementById('assessmentBatch').addEventListener('change', updateTotalWeightage);
    document.getElementById('weightage').addEventListener('input', updateTotalWeightage);
}

// ============================================
// Update Total Weightage
// ============================================
function updateTotalWeightage() {
    const batchId = parseInt(document.getElementById('assessmentBatch').value);
    const currentWeightage = parseFloat(document.getElementById('weightage').value) || 0;
    const display = document.getElementById('totalWeightage');
    
    if (!batchId) {
        display.textContent = '0%';
        display.className = 'total';
        return;
    }
    
    // Calculate total weightage for this batch excluding current assessment
    const batchAssessments = assessments.filter(a => 
        a.batchId === batchId && 
        a.id !== parseInt(document.getElementById('editAssessmentId').value)
    );
    
    const total = batchAssessments.reduce((sum, a) => sum + a.weightage, 0) + currentWeightage;
    display.textContent = `${Math.round(total)}%`;
    display.className = `total ${total > 100 ? 'exceeded' : 'within'}`;
}

// ============================================
// Populate Batch Select
// ============================================
function populateBatchSelect() {
    const select = document.getElementById('assessmentBatch');
    if (!select) return;
    
    select.innerHTML = '<option value="">Select Batch</option>';
    batches.forEach(batch => {
        const option = document.createElement('option');
        option.value = batch.id;
        option.textContent = batch.name;
        select.appendChild(option);
    });
}

// ============================================
// Render Table
// ============================================
function renderTable() {
    const tbody = document.getElementById('assessmentsTableBody');
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageAssessments = filteredAssessments.slice(start, end);
    
    if (pageAssessments.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center py-4 text-muted">
                    <i class="fas fa-tasks fa-2x d-block mb-2"></i>
                    No assessments found
                </td>
            </tr>
        `;
        document.getElementById('assessmentCount').textContent = '0';
        document.getElementById('tableInfo').textContent = 'Showing 0 of 0 assessments';
        return;
    }
    
    let html = '';
    pageAssessments.forEach((assessment, index) => {
        const batch = batches.find(b => b.id === assessment.batchId);
        const statusBadge = getAssessmentStatusBadge(assessment.status);
        const typeBadge = getAssessmentTypeBadge(assessment.type);
        
        html += `
            <tr>
                <td><span class="assessment-code">${assessment.code}</span></td>
                <td><strong>${assessment.title}</strong></td>
                <td>${typeBadge}</td>
                <td>${assessment.maxMarks}</td>
                <td>${assessment.weightage}%</td>
                <td>${formatDate(assessment.date)}</td>
                <td>${assessment.duration ? assessment.duration + 'm' : 'N/A'}</td>
                <td>${statusBadge}</td>
                <td>
                    <div class="dropdown actions-dropdown">
                        <button class="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
                            <i class="fas fa-ellipsis-v"></i>
                        </button>
                        <ul class="dropdown-menu">
                            <li>
                                <a class="dropdown-item" href="#" onclick="viewAssessment(${assessment.id})">
                                    <i class="fas fa-eye text-info"></i> View
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="#" onclick="editAssessment(${assessment.id})">
                                    <i class="fas fa-edit text-primary"></i> Edit
                                </a>
                            </li>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item text-danger" href="#" onclick="deleteAssessment(${assessment.id})">
                                    <i class="fas fa-trash"></i> Delete
                                </a>
                            </li>
                        </ul>
                    </div>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
    document.getElementById('assessmentCount').textContent = filteredAssessments.length;
    document.getElementById('tableInfo').textContent = 
        `Showing ${start + 1} to ${Math.min(end, filteredAssessments.length)} of ${filteredAssessments.length} assessments`;
    
    renderPagination();
}

function renderPagination() {
    const totalPages = Math.ceil(filteredAssessments.length / pageSize);
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
    const totalPages = Math.ceil(filteredAssessments.length / pageSize);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    renderTable();
}

// ============================================
// Filter and Search
// ============================================
function filterAssessments() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const typeFilter = document.getElementById('typeFilter').value;
    const statusFilter = document.getElementById('statusFilter').value;
    
    filteredAssessments = assessments.filter(assessment => {
        const matchSearch = assessment.title.toLowerCase().includes(search) || 
                           assessment.code.toLowerCase().includes(search);
        const matchType = !typeFilter || assessment.type === typeFilter;
        const matchStatus = !statusFilter || assessment.status === statusFilter;
        return matchSearch && matchType && matchStatus;
    });
    
    currentPage = 1;
    renderTable();
}

function resetFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('typeFilter').value = '';
    document.getElementById('statusFilter').value = '';
    filteredAssessments = [...assessments];
    currentPage = 1;
    renderTable();
}

function refreshTable() {
    filteredAssessments = [...assessments];
    currentPage = 1;
    renderTable();
    showAlert('Table refreshed', 'success');
}

// ============================================
// CRUD Operations
// ============================================

function saveAssessment() {
    const form = document.getElementById('assessmentForm');
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    const id = document.getElementById('editAssessmentId').value;
    const batchId = parseInt(document.getElementById('assessmentBatch').value);
    const weightage = parseFloat(document.getElementById('weightage').value);
    
    // Check total weightage
    const batchAssessments = assessments.filter(a => 
        a.batchId === batchId && 
        a.id !== parseInt(id)
    );
    const totalWeightage = batchAssessments.reduce((sum, a) => sum + a.weightage, 0) + weightage;
    
    if (totalWeightage > 100) {
        showAlert(`Total weightage (${Math.round(totalWeightage)}%) exceeds 100%`, 'danger');
        return;
    }
    
    const assessmentData = {
        title: document.getElementById('assessmentTitle').value.trim(),
        type: document.getElementById('assessmentType').value,
        batchId: batchId,
        maxMarks: parseInt(document.getElementById('maxMarks').value) || 0,
        weightage: weightage,
        passingMarks: parseInt(document.getElementById('passingMarks').value) || null,
        date: document.getElementById('assessmentDate').value,
        startTime: document.getElementById('startTime').value || null,
        endTime: document.getElementById('endTime').value || null,
        duration: parseInt(document.getElementById('duration').value) || null,
        totalQuestions: parseInt(document.getElementById('totalQuestions').value) || null,
        description: document.getElementById('assessmentDescription').value.trim(),
        instructions: document.getElementById('assessmentInstructions').value.trim(),
        status: document.getElementById('assessmentStatus').value,
        notes: document.getElementById('assessmentNotes').value.trim()
    };
    
    if (id) {
        const index = assessments.findIndex(a => a.id === parseInt(id));
        if (index !== -1) {
            assessments[index] = { ...assessments[index], ...assessmentData };
            showAlert('Assessment updated successfully!', 'success');
        }
    } else {
        const newAssessment = {
            id: Math.max(...assessments.map(a => a.id), 0) + 1,
            code: `A-2024-${String(assessments.length + 1).padStart(3, '0')}`,
            ...assessmentData
        };
        assessments.push(newAssessment);
        showAlert('Assessment created successfully!', 'success');
    }
    
    bootstrap.Modal.getInstance(document.getElementById('addAssessmentModal')).hide();
    filteredAssessments = [...assessments];
    renderTable();
    resetAssessmentForm();
}

function editAssessment(id) {
    const assessment = assessments.find(a => a.id === id);
    if (!assessment) return;
    
    document.getElementById('editAssessmentId').value = assessment.id;
    document.getElementById('assessmentModalTitle').textContent = 'Edit Assessment';
    document.getElementById('assessmentTitle').value = assessment.title;
    document.getElementById('assessmentType').value = assessment.type;
    document.getElementById('assessmentBatch').value = assessment.batchId;
    document.getElementById('maxMarks').value = assessment.maxMarks;
    document.getElementById('weightage').value = assessment.weightage;
    document.getElementById('passingMarks').value = assessment.passingMarks || '';
    document.getElementById('assessmentDate').value = assessment.date;
    document.getElementById('startTime').value = assessment.startTime || '';
    document.getElementById('endTime').value = assessment.endTime || '';
    document.getElementById('duration').value = assessment.duration || '';
    document.getElementById('totalQuestions').value = assessment.totalQuestions || '';
    document.getElementById('assessmentDescription').value = assessment.description || '';
    document.getElementById('assessmentInstructions').value = assessment.instructions || '';
    document.getElementById('assessmentStatus').value = assessment.status;
    document.getElementById('assessmentNotes').value = assessment.notes || '';
    
    updateTotalWeightage();
    
    const modal = new bootstrap.Modal(document.getElementById('addAssessmentModal'));
    modal.show();
}

function viewAssessment(id) {
    const assessment = assessments.find(a => a.id === id);
    if (!assessment) return;
    
    const body = document.getElementById('viewAssessmentBody');
    const batch = batches.find(b => b.id === assessment.batchId);
    const statusBadge = getAssessmentStatusBadge(assessment.status);
    const typeBadge = getAssessmentTypeBadge(assessment.type);
    
    body.innerHTML = `
        <div class="row">
            <div class="col-md-10 mx-auto">
                <div class="text-center mb-3">
                    <span class="assessment-code" style="font-size: 1.2rem;">${assessment.code}</span>
                    <h4 class="mt-2">${assessment.title}</h4>
                    ${typeBadge} ${statusBadge}
                </div>
                <hr>
                <div class="row">
                    <div class="col-6">
                        <small class="text-muted d-block">Batch</small>
                        <strong>${batch ? batch.name : 'N/A'}</strong>
                    </div>
                    <div class="col-6">
                        <small class="text-muted d-block">Date</small>
                        <strong>${formatDate(assessment.date)}</strong>
                    </div>
                </div>
                <hr>
                <div class="row">
                    <div class="col-4">
                        <small class="text-muted d-block">Max Marks</small>
                        <strong>${assessment.maxMarks}</strong>
                    </div>
                    <div class="col-4">
                        <small class="text-muted d-block">Weightage</small>
                        <strong>${assessment.weightage}%</strong>
                    </div>
                    <div class="col-4">
                        <small class="text-muted d-block">Passing Marks</small>
                        <strong>${assessment.passingMarks || `${Math.round(assessment.maxMarks * 0.5)} (50%)`}</strong>
                    </div>
                </div>
                <hr>
                <div class="row">
                    <div class="col-4">
                        <small class="text-muted d-block">Start Time</small>
                        <strong>${assessment.startTime || 'N/A'}</strong>
                    </div>
                    <div class="col-4">
                        <small class="text-muted d-block">End Time</small>
                        <strong>${assessment.endTime || 'N/A'}</strong>
                    </div>
                    <div class="col-4">
                        <small class="text-muted d-block">Duration</small>
                        <strong>${assessment.duration ? assessment.duration + ' minutes' : 'N/A'}</strong>
                    </div>
                </div>
                ${assessment.totalQuestions ? `
                <hr>
                <div class="row">
                    <div class="col-12">
                        <small class="text-muted d-block">Total Questions</small>
                        <strong>${assessment.totalQuestions}</strong>
                    </div>
                </div>` : ''}
                ${assessment.description ? `
                <hr>
                <div class="row">
                    <div class="col-12">
                        <small class="text-muted d-block">Description</small>
                        <p>${assessment.description}</p>
                    </div>
                </div>` : ''}
                ${assessment.instructions ? `
                <hr>
                <div class="row">
                    <div class="col-12">
                        <small class="text-muted d-block">Instructions</small>
                        <p>${assessment.instructions}</p>
                    </div>
                </div>` : ''}
                ${assessment.notes ? `
                <hr>
                <div class="row">
                    <div class="col-12">
                        <small class="text-muted d-block">Notes</small>
                        <p>${assessment.notes}</p>
                    </div>
                </div>` : ''}
            </div>
        </div>
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('viewAssessmentModal'));
    modal.show();
}

function deleteAssessment(id) {
    const assessment = assessments.find(a => a.id === id);
    if (!assessment) return;
    
    components.confirmAction(
        `Are you sure you want to delete assessment "${assessment.title}"?`,
        function() {
            assessments = assessments.filter(a => a.id !== id);
            filteredAssessments = [...assessments];
            renderTable();
            showAlert(`Assessment "${assessment.title}" deleted successfully`, 'success');
        }
    );
}

// ============================================
// Export Data
// ============================================
function exportData() {
    let csv = 'Code,Title,Type,Batch,Marks,Weightage,Date,Status\n';
    filteredAssessments.forEach(a => {
        const batch = batches.find(b => b.id === a.batchId);
        csv += `${a.code},${a.title},${a.type},${batch ? batch.name : 'N/A'},${a.maxMarks},${a.weightage}%,${a.date},${a.status}\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `assessments_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// ============================================
// Reset Form
// ============================================
function resetAssessmentForm() {
    document.getElementById('assessmentForm').reset();
    document.getElementById('assessmentForm').classList.remove('was-validated');
    document.getElementById('editAssessmentId').value = '';
    document.getElementById('assessmentModalTitle').textContent = 'Create New Assessment';
    document.getElementById('totalWeightage').textContent = '0%';
    document.getElementById('totalWeightage').className = 'total';
}

// ============================================
// Utility Functions
// ============================================
function getAssessmentStatusBadge(status) {
    const classes = {
        'Scheduled': 'badge-scheduled',
        'Ongoing': 'badge-ongoing',
        'Completed': 'badge-completed',
        'Cancelled': 'badge-cancelled'
    };
    const badgeClass = classes[status] || 'badge bg-secondary';
    return `<span class="badge ${badgeClass}">${status}</span>`;
}

function getAssessmentTypeBadge(type) {
    const classes = {
        'Quiz': 'quiz',
        'Assignment': 'assignment',
        'Lab': 'lab',
        'Practical': 'practical',
        'Project': 'project',
        'Exam': 'exam',
        'Presentation': 'presentation'
    };
    const cls = classes[type] || 'quiz';
    return `<span class="assessment-type-badge ${cls}">${type}</span>`;
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
    if (typeof assessments === 'undefined') {
        assessments = [];
    }
    filteredAssessments = [...assessments];
    renderTable();
    populateBatchSelect();
});
