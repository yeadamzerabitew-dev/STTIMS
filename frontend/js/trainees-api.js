/* ============================================
   STTIMS - Trainee Management with API
   ============================================ */

// Sample Trainees Data (will be replaced by API data)
let trainees = [];
let filteredTrainees = [];
let currentPage = 1;
const pageSize = 5;

// ============================================
// Initialize
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    loadTrainees();
    setupEventListeners();
});

// ============================================
// Setup Event Listeners
// ============================================
function setupEventListeners() {
    document.getElementById('saveTraineeBtn').addEventListener('click', saveTrainee);
    document.getElementById('searchInput').addEventListener('input', filterTrainees);
}

// ============================================
// Load Trainees from API
// ============================================
async function loadTrainees() {
    try {
        showLoading('Loading trainees...');
        
        const response = await STTIMS_API.TraineeAPI.list({
            page: currentPage,
            per_page: pageSize,
            status: document.getElementById('statusFilter')?.value || '',
            gender: document.getElementById('genderFilter')?.value || '',
            search: document.getElementById('searchInput')?.value || ''
        });
        
        trainees = response.trainees || [];
        filteredTrainees = trainees;
        
        renderTable();
        hideLoading();
    } catch (error) {
        hideLoading();
        showAlert('Failed to load trainees: ' + error.message, 'danger');
    }
}

// ============================================
// Save Trainee (Create/Update)
// ============================================
async function saveTrainee() {
    const form = document.getElementById('traineeForm');
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    const id = document.getElementById('editTraineeId').value;
    
    // Validate email uniqueness
    const email = document.getElementById('email').value.trim();
    if (!id && trainees.some(t => t.email === email)) {
        showAlert('Email already exists. Please use a different email.', 'danger');
        return;
    }
    
    // Validate phone
    const phone = document.getElementById('phone').value.trim();
    if (!/^09\d{8}$/.test(phone)) {
        showAlert('Phone number must be 10 digits starting with 09', 'danger');
        return;
    }
    
    const traineeData = {
        first_name: document.getElementById('firstName').value.trim(),
        middle_name: document.getElementById('middleName').value.trim(),
        last_name: document.getElementById('lastName').value.trim(),
        gender: document.getElementById('gender').value,
        date_of_birth: document.getElementById('dateOfBirth').value,
        email: email,
        phone_number: phone,
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
        showLoading('Saving trainee...');
        
        let response;
        if (id) {
            // Update existing trainee
            response = await STTIMS_API.TraineeAPI.update(id, traineeData);
            showAlert('Trainee updated successfully!', 'success');
        } else {
            // Create new trainee
            response = await STTIMS_API.TraineeAPI.create(traineeData);
            showAlert('Trainee created successfully!', 'success');
        }
        
        // Close modal and refresh
        bootstrap.Modal.getInstance(document.getElementById('addTraineeModal')).hide();
        await loadTrainees();
        resetTraineeForm();
        hideLoading();
    } catch (error) {
        hideLoading();
        showAlert('Failed to save trainee: ' + error.message, 'danger');
    }
}

// ============================================
// Edit Trainee
// ============================================
async function editTrainee(id) {
    try {
        showLoading('Loading trainee data...');
        
        const response = await STTIMS_API.TraineeAPI.get(id);
        const trainee = response.trainee;
        
        if (!trainee) {
            showAlert('Trainee not found', 'danger');
            hideLoading();
            return;
        }
        
        document.getElementById('editTraineeId').value = trainee.trainee_id;
        document.getElementById('traineeModalTitle').textContent = 'Edit Trainee';
        document.getElementById('firstName').value = trainee.first_name;
        document.getElementById('middleName').value = trainee.middle_name || '';
        document.getElementById('lastName').value = trainee.last_name;
        document.getElementById('gender').value = trainee.gender;
        document.getElementById('dateOfBirth').value = trainee.date_of_birth;
        document.getElementById('email').value = trainee.email;
        document.getElementById('phone').value = trainee.phone_number;
        document.getElementById('altPhone').value = trainee.alternative_phone || '';
        document.getElementById('address').value = trainee.address || '';
        document.getElementById('city').value = trainee.city || '';
        document.getElementById('region').value = trainee.state_region || '';
        document.getElementById('educationLevel').value = trainee.educational_level;
        document.getElementById('occupation').value = trainee.occupation || '';
        document.getElementById('organization').value = trainee.organization || '';
        document.getElementById('guardianName').value = trainee.emergency_contact_name;
        document.getElementById('relationship').value = trainee.relationship || 'Father';
        document.getElementById('guardianPhone').value = trainee.emergency_contact_phone;
        document.getElementById('traineeStatus').value = trainee.status;
        
        // Reset image
        document.getElementById('imagePreview').classList.remove('show');
        document.getElementById('imagePlaceholder').style.display = 'block';
        
        hideLoading();
        const modal = new bootstrap.Modal(document.getElementById('addTraineeModal'));
        modal.show();
    } catch (error) {
        hideLoading();
        showAlert('Failed to load trainee: ' + error.message, 'danger');
    }
}

// ============================================
// Delete Trainee
// ============================================
function deleteTrainee(id) {
    const trainee = trainees.find(t => t.trainee_id === id);
    if (!trainee) return;
    
    components.confirmAction(
        `Are you sure you want to delete trainee "${trainee.first_name} ${trainee.last_name}"?`,
        async function() {
            try {
                showLoading('Deleting trainee...');
                await STTIMS_API.TraineeAPI.delete(id);
                await loadTrainees();
                showAlert('Trainee deleted successfully', 'success');
                hideLoading();
            } catch (error) {
                hideLoading();
                showAlert('Failed to delete trainee: ' + error.message, 'danger');
            }
        }
    );
}

// ============================================
// Filter Trainees
// ============================================
function filterTrainees() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter')?.value || '';
    const genderFilter = document.getElementById('genderFilter')?.value || '';
    
    filteredTrainees = trainees.filter(trainee => {
        const fullName = `${trainee.first_name} ${trainee.middle_name || ''} ${trainee.last_name}`.toLowerCase();
        const matchSearch = fullName.includes(search) || 
                           trainee.trainee_code.toLowerCase().includes(search) ||
                           trainee.email.toLowerCase().includes(search);
        const matchStatus = !statusFilter || trainee.status === statusFilter;
        const matchGender = !genderFilter || trainee.gender === genderFilter;
        return matchSearch && matchStatus && matchGender;
    });
    
    currentPage = 1;
    renderTable();
}

// ============================================
// Render Table
// ============================================
function renderTable() {
    const tbody = document.getElementById('traineesTableBody');
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageTrainees = filteredTrainees.slice(start, end);
    
    if (pageTrainees.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center py-4 text-muted">
                    <i class="fas fa-user-graduate fa-2x d-block mb-2"></i>
                    No trainees found
                </td>
            </tr>
        `;
        document.getElementById('traineeCount').textContent = '0';
        document.getElementById('tableInfo').textContent = 'Showing 0 of 0 trainees';
        return;
    }
    
    let html = '';
    pageTrainees.forEach((trainee, index) => {
        const fullName = `${trainee.first_name} ${trainee.middle_name || ''} ${trainee.last_name}`;
        const statusBadge = getStatusBadge(trainee.status);
        
        html += `
            <tr>
                <td>
                    <div class="trainee-avatar-placeholder" style="width:45px;height:45px;border-radius:50%;background:linear-gradient(135deg,#4F46E5,#7C3AED);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:600;font-size:1rem;">
                        ${getInitials(trainee.first_name, trainee.last_name)}
                    </div>
                </td>
                <td><span class="trainee-code">${trainee.trainee_code}</span></td>
                <td><strong>${fullName}</strong></td>
                <td>${trainee.email}</td>
                <td>${trainee.phone_number}</td>
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
    document.getElementById('traineeCount').textContent = filteredTrainees.length;
    document.getElementById('tableInfo').textContent = 
        `Showing ${start + 1} to ${Math.min(end, filteredTrainees.length)} of ${filteredTrainees.length} trainees`;
    
    renderPagination();
}

function renderPagination() {
    const totalPages = Math.ceil(filteredTrainees.length / pageSize);
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
    const totalPages = Math.ceil(filteredTrainees.length / pageSize);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    renderTable();
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
    return `<span class="badge ${badgeClass}">${status}</span>`;
}

function getInitials(firstName, lastName) {
    if (!firstName && !lastName) return 'U';
    return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`.toUpperCase();
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

function showLoading(message = 'Loading...') {
    components.showLoading(message);
}

function hideLoading() {
    components.hideLoading();
}

function resetTraineeForm() {
    document.getElementById('traineeForm').reset();
    document.getElementById('traineeForm').classList.remove('was-validated');
    document.getElementById('editTraineeId').value = '';
    document.getElementById('traineeModalTitle').textContent = 'Add New Trainee';
    document.getElementById('imagePreview').classList.remove('show');
    document.getElementById('imagePlaceholder').style.display = 'block';
}

// ============================================
// Initialize on page load
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    loadTrainees();
    setupEventListeners();
});
