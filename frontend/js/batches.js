/**
 * Batch Management - API Version
 */

import { BatchAPI } from './api.js';

let batches = [];
let filteredBatches = [];
let currentPage = 1;
const pageSize = 10;

async function loadBatches() {
    try {
        const response = await BatchAPI.getAll();
        if (response.status === 'success' && response.data) {
            batches = response.data;
            filteredBatches = [...batches];
            renderTable();
            updateStats();
        }
    } catch (error) {
        console.error('Error loading batches:', error);
        showAlert('Error loading batches', 'danger');
    }
}

function renderTable() {
    const tbody = document.getElementById('batchesTableBody');
    if (!tbody) return;
    
    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageBatches = filteredBatches.slice(start, end);
    
    if (pageBatches.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center">No batches found</td></tr>`;
        return;
    }
    
    let html = '';
    pageBatches.forEach(b => {
        html += `
            <tr>
                <td>${b.batch_code || 'N/A'}</td>
                <td>${b.batch_name || 'N/A'}</td>
                <td>${b.start_date ? new Date(b.start_date).toLocaleDateString() : 'N/A'}</td>
                <td>${b.end_date ? new Date(b.end_date).toLocaleDateString() : 'N/A'}</td>
                <td>${b.max_capacity || 0}</td>
                <td><span class="badge ${b.status === 'Ongoing' ? 'bg-success' : b.status === 'Upcoming' ? 'bg-warning' : 'bg-secondary'}">${b.status || 'N/A'}</span></td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

function updateStats() {
    const countEl = document.getElementById('batchCount');
    if (countEl) countEl.textContent = batches.length;
}

function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    if (!container) return;
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => container.innerHTML = '', 3000);
}

document.addEventListener('DOMContentLoaded', loadBatches);
