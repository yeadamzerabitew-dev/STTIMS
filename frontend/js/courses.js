/**
 * Course Management - API Version
 */

import { CourseAPI } from './api.js';

let courses = [];
let filteredCourses = [];
let currentPage = 1;
const pageSize = 10;

async function loadCourses() {
    try {
        const response = await CourseAPI.getAll();
        if (response.status === 'success' && response.data) {
            courses = response.data;
            filteredCourses = [...courses];
            renderTable();
            updateStats();
        }
    } catch (error) {
        console.error('Error loading courses:', error);
        showAlert('Error loading courses', 'danger');
    }
}

function renderTable() {
    const tbody = document.getElementById('coursesTableBody');
    if (!tbody) return;
    
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageCourses = filteredCourses.slice(start, end);
    
    if (pageCourses.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center">No courses found</td></tr>`;
        return;
    }
    
    let html = '';
    pageCourses.forEach(c => {
        html += `
            <tr>
                <td>${c.course_code || 'N/A'}</td>
                <td>${c.course_title || 'N/A'}</td>
                <td>${c.duration_hours || 0} hrs</td>
                <td>${c.fee_amount || 0} ${c.fee_currency || 'ETB'}</td>
                <td>${c.course_level || 'N/A'}</td>
                <td>${c.max_capacity || 0}</td>
                <td><span class="badge ${c.status === 'Active' ? 'bg-success' : 'bg-secondary'}">${c.status || 'N/A'}</span></td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

function updateStats() {
    const countEl = document.getElementById('courseCount');
    if (countEl) countEl.textContent = courses.length;
}

function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    if (!container) return;
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => container.innerHTML = '', 3000);
}

document.addEventListener('DOMContentLoaded', loadCourses);
