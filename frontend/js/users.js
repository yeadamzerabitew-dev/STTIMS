/**
 * User Management - API Version
 */

import { UserAPI } from './api.js';

let users = [];
let filteredUsers = [];
let currentPage = 1;
const pageSize = 10;

async function loadUsers() {
    try {
        const response = await UserAPI.getAll();
        if (response.status === 'success' && response.data) {
            users = response.data;
            filteredUsers = [...users];
            renderTable();
            updateStats();
        }
    } catch (error) {
        console.error('Error loading users:', error);
        showAlert('Error loading users', 'danger');
    }
}

function renderTable() {
    const tbody = document.getElementById('usersTableBody');
    if (!tbody) return;
    
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageUsers = filteredUsers.slice(start, end);
    
    if (pageUsers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center">No users found</td></tr>`;
        return;
    }
    
    let html = '';
    pageUsers.forEach(u => {
        html += `
            <tr>
                <td>${u.username || 'N/A'}</td>
                <td>${u.email || 'N/A'}</td>
                <td><span class="badge bg-info">${u.role || 'N/A'}</span></td>
                <td><span class="badge ${u.status === 'Active' ? 'bg-success' : 'bg-secondary'}">${u.status || 'N/A'}</span></td>
                <td>
                    <button class="btn btn-sm btn-warning"><i class="fas fa-edit"></i></button>
                    <button class="btn btn-sm btn-danger"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

function updateStats() {
    const countEl = document.getElementById('userCount');
    if (countEl) countEl.textContent = users.length;
}

function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    if (!container) return;
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => container.innerHTML = '', 3000);
}

document.addEventListener('DOMContentLoaded', loadUsers);
