/**
 * Trainee Management - API Version
 * Uses real data from the backend
 */

import { TraineeAPI } from './api.js';

let trainees = [];
let filteredTrainees = [];
let currentPage = 1;
const pageSize = 10;

// ============================================
// Load Trainees from API
// ============================================
async function loadTrainees() {
    try {
        showLoading(true);
        const response = await TraineeAPI.getAll();
        if (response.status === 'success' && response.data) {
            trainees = response.data;
            filteredTrainees = [...trainees];
            renderTable();
            updateStats();
        } else {
            showAlert('Failed to load trainees', 'danger');
        }
    } catch (error) {
        console.error('Error loading trainees:', error);
        showAlert('Error loading trainees: ' + error.message, 'danger');
    } finally {
        showLoading(false);
    }
}

// ============================================
// Render Table
// ============================================
function renderTable() {
    const tbody = document.getElementById('traineesTableBody');
    if (!tbody) return;
    
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageTrainees = filteredTrainees.slice(start, end);
    
    if (pageTrainees.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center py-4 text-muted">
                    <i class="fas fa-user-graduate fa-2x d-block mb-2"></i>
                    No trainees found
                </td>
            </tr>
        `;
        return;
    }
    
    let html = '';
    pageTrainees.forEach(trainee => {
        const fullName = `${trainee.first_name || ''} ${trainee.middle_name || ''} ${trainee.last_name || ''}`.trim();
        const statusBadge = getStatusBadge(trainee.status);
        const avatarHtml = trainee.profile_image 
            ? `<img src="${trainee.profile_image}" alt="${fullName}" class="trainee-avatar" style="width:40px;height:40px;border-radius:50%;object-fit:cover;">`
            : `<div class="trainee-avatar-placeholder" style="width:40px;height:40px;border-radius:50%;background:#4F46E5;color:white;display:flex;align-items:center;justify-content:center;font-weight:bold;">${getInitials(trainee.first_name, trainee.last_name)}</div>`;
        
        html += `
            <tr>
                <td>${avatarHtml}</td>
                <td><span class="trainee-code">${trainee.trainee_code || 'N/A'}</span></td>
                <td><strong>${fullName}</strong></td>
                <td>${trainee.email || 'N/A'}</td>
                <td>${trainee.phone_number || 'N/A'}</td>
                <td>${trainee.educational_level || 'N/A'}</td>
                <td>${statusBadge}</td>
                <td>
                    <div class="dropdown actions-dropdown">
                        <button class="btn btn-sm btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown">
                            <i class="fas fa-ellipsis-v"></i>
                        </button>
                        <ul class="dropdown-menu">
                            <li>
                                <a class="dropdown-item" href="#" onclick="viewTrainee(${trainee.trainee_id})">
                                    <i class="fas fa-eye text-info"></i> View
                                </a>
                            </li>
                            <li>
                                <a class="dropdown-item" href="#" onclick="editTrainee(${trainee.trainee_id})">
                                    <i class="fas fa-edit text-primary"></i> Edit
                                </a>
                            </li>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item text-danger" href="#" onclick="deleteTrainee(${trainee.trainee_id})">
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
    renderPagination();
}

function renderPagination() {
    const container = document.getElementById('paginationContainer');
    if (!container) return;
    
    const totalPages = Math.ceil(filteredTrainees.length / pageSize);
    if (totalPages <= 1) {
        container.innerHTML = '';
        return;
    }
    
    let html = `<ul class="pagination pagination-sm mb-0">`;
    html += `<li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="goToPage(${currentPage - 1})">Previous</a>
            </li>`;
    
    for (let i = 1; i <= totalPages; i++) {
        html += `<li class="page-item ${i === currentPage ? 'active' : ''}">
                    <a class="page-link" href="#" onclick="goToPage(${i})">${i}</a>
                </li>`;
    }
    
    html += `<li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" onclick="goToPage(${currentPage + 1})">Next</a>
            </li>`;
    html += `</ul>`;
    
    container.innerHTML = html;
}

function goToPage(page) {
    const totalPages = Math.ceil(filteredTrainees.length / pageSize);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    renderTable();
}

// ============================================
// Filter and Search
// ============================================
function filterTrainees() {
    const search = document.getElementById('searchInput')?.value?.toLowerCase() || '';
    const statusFilter = document.getElementById('statusFilter')?.value || '';
    const genderFilter = document.getElementById('genderFilter')?.value || '';
    
    filteredTrainees = trainees.filter(trainee => {
        const fullName = `${trainee.first_name || ''} ${trainee.middle_name || ''} ${trainee.last_name || ''}`.toLowerCase();
        const matchSearch = fullName.includes(search) || 
                           (trainee.trainee_code || '').toLowerCase().includes(search) ||
                           (trainee.email || '').toLowerCase().includes(search);
        const matchStatus = !statusFilter || trainee.status === statusFilter;
        const matchGender = !genderFilter || trainee.gender === genderFilter;
        return matchSearch && matchStatus && matchGender;
    });
    
    currentPage = 1;
    renderTable();
}

function resetFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('statusFilter').value = '';
    document.getElementById('genderFilter').value = '';
    filteredTrainees = [...trainees];
    currentPage = 1;
    renderTable();
}

// ============================================
// CRUD Operations
// ============================================
async function saveTrainee() {
    const form = document.getElementById('traineeForm');
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    const id = document.getElementById('editTraineeId').value;
    
    const traineeData = {
        first_name: document.getElementById('firstName').value.trim(),
        middle_name: document.getElementById('middleName').value.trim(),
        last_name: document.getElementById('lastName').value.trim(),
        gender: document.getElementById('gender').value,
        date_of_birth: document.getElementById('dateOfBirth').value,
        email: document.getElementById('email').value.trim(),
        phone_number: document.getElementById('phone').value.trim(),
        alternative_phone: document.getElementById('altPhone').value.trim(),
        address: document.getElementById('address').value.trim(),
        city: document.getElementById('city').value.trim(),
        state_region: document.getElementById('region').value.trim(),
        educational_level: document.getElementById('educationLevel').value,
        occupation: document.getElementById('occupation').value.trim(),
        organization: document.getElementById('organization').value.trim(),
        emergency_contact_name: document.getElementById('guardianName').value.trim(),
        emergency_contact_phone: document.getElementById('guardianPhone').value.trim(),
        status: document.getElementById('traineeStatus').value
    };
    
    try {
        let response;
        if (id) {
            response = await TraineeAPI.update(parseInt(id), traineeData);
        } else {
            response = await TraineeAPI.create(traineeData);
        }
        
        if (response.status === 'success') {
            showAlert(id ? 'Trainee updated successfully!' : 'Trainee created successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addTraineeModal')).hide();
            await loadTrainees();
            resetTraineeForm();
        } else {
            showAlert(response.message || 'Failed to save trainee', 'danger');
        }
    } catch (error) {
        console.error('Error saving trainee:', error);
        showAlert('Error: ' + error.message, 'danger');
    }
}

async function viewTrainee(id) {
    try {
        const response = await TraineeAPI.get(id);
        if (response.status === 'success' && response.data) {
            const t = response.data;
            const body = document.getElementById('viewTraineeBody');
            const fullName = `${t.first_name || ''} ${t.middle_name || ''} ${t.last_name || ''}`.trim();
            const statusBadge = getStatusBadge(t.status);
            
            body.innerHTML = `
                <div class="row">
                    <div class="col-md-4 text-center">
                        <div class="trainee-avatar-placeholder mx-auto" style="width: 120px; height: 120px; font-size: 2.5rem; border-radius: 50%; background: #4F46E5; color: white; display: flex; align-items: center; justify-content: center;">
                            ${getInitials(t.first_name, t.last_name)}
                        </div>
                        <h5 class="mt-2">${fullName}</h5>
                        <span class="trainee-code">${t.trainee_code || 'N/A'}</span>
                        <div class="mt-2">${statusBadge}</div>
                    </div>
                    <div class="col-md-8">
                        <div class="row">
                            <div class="col-6">
                                <small class="text-muted d-block">Email</small>
                                <strong>${t.email || 'N/A'}</strong>
                            </div>
                            <div class="col-6">
                                <small class="text-muted d-block">Phone</small>
                                <strong>${t.phone_number || 'N/A'}</strong>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-6">
                                <small class="text-muted d-block">Gender</small>
                                <strong>${t.gender || 'N/A'}</strong>
                            </div>
                            <div class="col-6">
                                <small class="text-muted d-block">Date of Birth</small>
                                <strong>${t.date_of_birth ? new Date(t.date_of_birth).toLocaleDateString() : 'N/A'}</strong>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-6">
                                <small class="text-muted d-block">Education</small>
                                <strong>${t.educational_level || 'N/A'}</strong>
                            </div>
                            <div class="col-6">
                                <small class="text-muted d-block">Occupation</small>
                                <strong>${t.occupation || 'N/A'}</strong>
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-6">
                                <small class="text-muted d-block">Guardian</small>
                                <strong>${t.emergency_contact_name || 'N/A'}</strong>
                            </div>
                            <div class="col-6">
                                <small class="text-muted d-block">Guardian Phone</small>
                                <strong>${t.emergency_contact_phone || 'N/A'}</strong>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            const modal = new bootstrap.Modal(document.getElementById('viewTraineeModal'));
            modal.show();
        }
    } catch (error) {
        console.error('Error viewing trainee:', error);
        showAlert('Error loading trainee details', 'danger');
    }
}

async function editTrainee(id) {
    try {
        const response = await TraineeAPI.get(id);
        if (response.status === 'success' && response.data) {
            const t = response.data;
            
            document.getElementById('editTraineeId').value = t.trainee_id;
            document.getElementById('traineeModalTitle').textContent = 'Edit Trainee';
            document.getElementById('firstName').value = t.first_name || '';
            document.getElementById('middleName').value = t.middle_name || '';
            document.getElementById('lastName').value = t.last_name || '';
            document.getElementById('gender').value = t.gender || '';
            document.getElementById('dateOfBirth').value = t.date_of_birth || '';
            document.getElementById('email').value = t.email || '';
            document.getElementById('phone').value = t.phone_number || '';
            document.getElementById('altPhone').value = t.alternative_phone || '';
            document.getElementById('address').value = t.address || '';
            document.getElementById('city').value = t.city || '';
            document.getElementById('region').value = t.state_region || '';
            document.getElementById('educationLevel').value = t.educational_level || '';
            document.getElementById('occupation').value = t.occupation || '';
            document.getElementById('organization').value = t.organization || '';
            document.getElementById('guardianName').value = t.emergency_contact_name || '';
            document.getElementById('guardianPhone').value = t.emergency_contact_phone || '';
            document.getElementById('traineeStatus').value = t.status || 'Active';
            
            const modal = new bootstrap.Modal(document.getElementById('addTraineeModal'));
            modal.show();
        }
    } catch (error) {
        console.error('Error loading trainee for edit:', error);
        showAlert('Error loading trainee details', 'danger');
    }
}

async function deleteTrainee(id) {
    const trainee = trainees.find(t => t.trainee_id === id);
    if (!trainee) return;
    
    if (confirm(`Are you sure you want to delete trainee "${trainee.first_name} ${trainee.last_name}"?`)) {
        try {
            const response = await TraineeAPI.delete(id);
            if (response.status === 'success') {
                showAlert('Trainee deleted successfully', 'success');
                await loadTrainees();
            } else {
                showAlert(response.message || 'Failed to delete trainee', 'danger');
            }
        } catch (error) {
            console.error('Error deleting trainee:', error);
            showAlert('Error: ' + error.message, 'danger');
        }
    }
}

// ============================================
// Utility Functions
// ============================================
function getStatusBadge(status) {
    const classes = {
        'Active': 'badge-active',
        'Inactive': 'badge-inactive',
        'Suspended': 'badge-inactive'
    };
    const badgeClass = classes[status] || 'badge bg-secondary';
    return `<span class="badge ${badgeClass}">${status || 'N/A'}</span>`;
}

function getInitials(firstName, lastName) {
    if (!firstName && !lastName) return 'U';
    return `${(firstName || '')[0] || ''}${(lastName || '')[0] || ''}`.toUpperCase() || 'U';
}

function showAlert(message, type = 'info') {
    const container = document.getElementById('alertContainer');
    if (!container) return;
    
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

function showLoading(show) {
    const loader = document.getElementById('loadingSpinner');
    if (loader) {
        loader.style.display = show ? 'block' : 'none';
    }
}

function updateStats() {
    const countElement = document.getElementById('traineeCount');
    if (countElement) {
        countElement.textContent = trainees.length;
    }
}

function resetTraineeForm() {
    document.getElementById('traineeForm').reset();
    document.getElementById('traineeForm').classList.remove('was-validated');
    document.getElementById('editTraineeId').value = '';
    document.getElementById('traineeModalTitle').textContent = 'Add New Trainee';
}

function refreshTable() {
    loadTrainees();
}

function exportData() {
    showAlert('Exporting data...', 'info');
    // Implementation for CSV export
    if (filteredTrainees.length === 0) {
        showAlert('No data to export', 'warning');
        return;
    }
    
    const headers = ['Code', 'Full Name', 'Email', 'Phone', 'Gender', 'Status'];
    const rows = filteredTrainees.map(t => [
        t.trainee_code || '',
        `${t.first_name || ''} ${t.middle_name || ''} ${t.last_name || ''}`.trim(),
        t.email || '',
        t.phone_number || '',
        t.gender || '',
        t.status || ''
    ]);
    
    let csv = headers.join(',') + '\n';
    rows.forEach(row => {
        csv += row.map(cell => `"${cell}"`).join(',') + '\n';
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `trainees_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}

// ============================================
// Initialize on page load
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // Setup event listeners
    document.getElementById('searchInput')?.addEventListener('input', filterTrainees);
    document.getElementById('statusFilter')?.addEventListener('change', filterTrainees);
    document.getElementById('genderFilter')?.addEventListener('change', filterTrainees);
    document.getElementById('saveTraineeBtn')?.addEventListener('click', saveTrainee);
    document.getElementById('resetBtn')?.addEventListener('click', resetFilters);
    
    // Load data
    loadTrainees();
});

// Make functions globally accessible for inline onclick handlers
window.viewTrainee = viewTrainee;
window.editTrainee = editTrainee;
window.deleteTrainee = deleteTrainee;
window.goToPage = goToPage;
window.filterTrainees = filterTrainees;
window.resetFilters = resetFilters;
window.refreshTable = refreshTable;
window.exportData = exportData;
window.saveTrainee = saveTrainee;
