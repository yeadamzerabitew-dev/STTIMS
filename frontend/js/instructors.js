/**
 * Instructor Management - API Version
 */

import { InstructorAPI } from './api.js';

let instructors = [];
let filteredInstructors = [];
let currentPage = 1;
const pageSize = 10;

async function loadInstructors() {
    try {
        const response = await InstructorAPI.getAll();
        if (response.status === 'success' && response.data) {
            instructors = response.data;
            filteredInstructors = [...instructors];
            renderTable();
            updateStats();
        }
    } catch (error) {
        console.error('Error loading instructors:', error);
        showAlert('Error loading instructors', 'danger');
    }
}

function renderTable() {
    const tbody = document.getElementById('instructorsTableBody');
    if (!tbody) return;
    
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageInstructors = filteredInstructors.slice(start, end);
    
    if (pageInstructors.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center">No instructors found</td></tr>`;
        return;
    }
    
    let html = '';
    pageInstructors.forEach(i => {
        const fullName = `${i.first_name || ''} ${i.middle_name || ''} ${i.last_name || ''}`.trim();
        html += `
            <tr>
                <td>${i.instructor_code || 'N/A'}</td>
                <td>${fullName}</td>
                <td>${i.email || 'N/A'}</td>
                <td>${i.phone_number || 'N/A'}</td>
                <td>${i.department || 'N/A'}</td>
                <td>${i.years_of_experience || 0} yrs</td>
                <td><span class="badge ${i.status === 'Active' ? 'bg-success' : 'bg-secondary'}">${i.status || 'N/A'}</span></td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

function updateStats() {
    const countEl = document.getElementById('instructorCount');
    if (countEl) countEl.textContent = instructors.length;
}

function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    if (!container) return;
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => container.innerHTML = '', 3000);
}

document.addEventListener('DOMContentLoaded', loadInstructors);
