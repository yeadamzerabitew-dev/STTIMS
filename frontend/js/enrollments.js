/**
 * Enrollment Management - API Version
 */

import { EnrollmentAPI } from './api.js';

let enrollments = [];
let filteredEnrollments = [];
let currentPage = 1;
const pageSize = 10;

async function loadEnrollments() {
    try {
        const response = await EnrollmentAPI.getAll();
        if (response.status === 'success' && response.data) {
            enrollments = response.data;
            filteredEnrollments = [...enrollments];
            renderTable();
            updateStats();
        }
    } catch (error) {
        console.error('Error loading enrollments:', error);
        showAlert('Error loading enrollments', 'danger');
    }
}

function renderTable() {
    const tbody = document.getElementById('enrollmentsTableBody');
    if (!tbody) return;
    
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageEnrollments = filteredEnrollments.slice(start, end);
    
    if (pageEnrollments.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center">No enrollments found</td></tr>`;
        return;
    }
    
    let html = '';
    pageEnrollments.forEach(e => {
        html += `
            <tr>
                <td>${e.enrollment_number || 'N/A'}</td>
                <td>${e.trainee_id || 'N/A'}</td>
                <td>${e.batch_id || 'N/A'}</td>
                <td>${e.enrollment_date ? new Date(e.enrollment_date).toLocaleDateString() : 'N/A'}</td>
                <td><span class="badge ${e.status === 'Active' ? 'bg-success' : 'bg-warning'}">${e.status || 'N/A'}</span></td>
                <td><span class="badge ${e.payment_status === 'Paid' ? 'bg-success' : 'bg-warning'}">${e.payment_status || 'N/A'}</span></td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

function updateStats() {
    const countEl = document.getElementById('enrollmentCount');
    if (countEl) countEl.textContent = enrollments.length;
}

function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    if (!container) return;
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => container.innerHTML = '', 3000);
}

document.addEventListener('DOMContentLoaded', loadEnrollments);
