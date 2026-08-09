/**
 * Trainee Management - API Version
 */

import { TraineeAPI } from './api.js';

let trainees = [];
let filteredTrainees = [];
let currentPage = 1;
const pageSize = 10;

async function loadTrainees() {
    try {
        const response = await TraineeAPI.getAll();
        if (response.status === 'success' && response.data) {
            trainees = response.data;
            filteredTrainees = [...trainees];
            renderTable();
            updateStats();
        }
    } catch (error) {
        console.error('Error loading trainees:', error);
        showAlert('Error loading trainees', 'danger');
    }
}

function renderTable() {
    const tbody = document.getElementById('traineesTableBody');
    if (!tbody) return;
    
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageTrainees = filteredTrainees.slice(start, end);
    
    if (pageTrainees.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center">No trainees found</td></tr>`;
        return;
    }
    
    let html = '';
    pageTrainees.forEach(t => {
        const fullName = `${t.first_name || ''} ${t.middle_name || ''} ${t.last_name || ''}`.trim();
        html += `
            <tr>
                <td>${t.trainee_code || 'N/A'}</td>
                <td>${fullName}</td>
                <td>${t.email || 'N/A'}</td>
                <td>${t.phone_number || 'N/A'}</td>
                <td>${t.gender || 'N/A'}</td>
                <td><span class="badge ${t.status === 'Active' ? 'bg-success' : 'bg-secondary'}">${t.status || 'N/A'}</span></td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="viewTrainee(${t.trainee_id})"><i class="fas fa-eye"></i></button>
                    <button class="btn btn-sm btn-warning" onclick="editTrainee(${t.trainee_id})"><i class="fas fa-edit"></i></button>
                    <button class="btn btn-sm btn-danger" onclick="deleteTrainee(${t.trainee_id})"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

function updateStats() {
    const countEl = document.getElementById('traineeCount');
    if (countEl) countEl.textContent = trainees.length;
}

function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    if (!container) return;
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => container.innerHTML = '', 3000);
}

// Global functions for HTML onclick
window.viewTrainee = async (id) => {
    try {
        const response = await TraineeAPI.get(id);
        if (response.status === 'success') {
            alert(JSON.stringify(response.data, null, 2));
        }
    } catch (error) {
        showAlert('Error loading trainee', 'danger');
    }
};

window.editTrainee = async (id) => {
    try {
        const response = await TraineeAPI.get(id);
        if (response.status === 'success') {
            const t = response.data;
            document.getElementById('editTraineeId').value = t.trainee_id;
            document.getElementById('firstName').value = t.first_name || '';
            document.getElementById('lastName').value = t.last_name || '';
            document.getElementById('email').value = t.email || '';
            document.getElementById('phone').value = t.phone_number || '';
            // Open modal
            const modal = new bootstrap.Modal(document.getElementById('addTraineeModal'));
            modal.show();
        }
    } catch (error) {
        showAlert('Error loading trainee', 'danger');
    }
};

window.deleteTrainee = async (id) => {
    if (confirm('Are you sure?')) {
        try {
            await TraineeAPI.delete(id);
            showAlert('Trainee deleted', 'success');
            loadTrainees();
        } catch (error) {
            showAlert('Error deleting trainee', 'danger');
        }
    }
};

window.saveTrainee = async () => {
    const id = document.getElementById('editTraineeId').value;
    const data = {
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        phone_number: document.getElementById('phone').value,
        gender: document.getElementById('gender').value,
        date_of_birth: document.getElementById('dateOfBirth').value,
        educational_level: document.getElementById('educationLevel').value,
        emergency_contact_name: document.getElementById('guardianName').value,
        emergency_contact_phone: document.getElementById('guardianPhone').value,
        status: document.getElementById('traineeStatus').value
    };
    
    try {
        if (id) {
            await TraineeAPI.update(id, data);
            showAlert('Trainee updated', 'success');
        } else {
            await TraineeAPI.create(data);
            showAlert('Trainee created', 'success');
        }
        bootstrap.Modal.getInstance(document.getElementById('addTraineeModal')).hide();
        loadTrainees();
    } catch (error) {
        showAlert('Error saving trainee', 'danger');
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', loadTrainees);
