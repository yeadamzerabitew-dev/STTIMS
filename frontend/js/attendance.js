/* ============================================
   STTIMS - Attendance Management JavaScript
   ============================================ */

// Sample Data
const batches = [
    { id: 1, name: 'Python Batch 1' },
    { id: 2, name: 'Python Batch 2' },
    { id: 3, name: 'Electrical Safety Weekend' },
    { id: 4, name: 'Web Development PHP Batch 1' }
];

const sessions = [
    { id: 1, batchId: 1, date: '2024-02-01', topic: 'Introduction to Python' },
    { id: 2, batchId: 1, date: '2024-02-03', topic: 'Python Syntax and Data Types' },
    { id: 3, batchId: 1, date: '2024-02-05', topic: 'Control Structures' },
    { id: 4, batchId: 3, date: '2024-02-17', topic: 'Introduction to Electrical Safety' },
    { id: 5, batchId: 4, date: '2024-03-01', topic: 'PHP Basics' }
];

const trainees = [
    { id: 1, code: 'T-2024-001', name: 'Abebe Tesfaye', status: 'Active' },
    { id: 2, code: 'T-2024-002', name: 'Birtukan Wolde', status: 'Active' },
    { id: 3, code: 'T-2024-003', name: 'Chala Hailu', status: 'Active' },
    { id: 4, code: 'T-2024-004', name: 'Desta Bekele', status: 'Active' },
    { id: 5, code: 'T-2024-005', name: 'Emebet Girma', status: 'Active' },
    { id: 6, code: 'T-2024-006', name: 'Fikre Ayele', status: 'Active' },
    { id: 7, code: 'T-2024-007', name: 'Genet Assefa', status: 'Active' },
    { id: 8, code: 'T-2024-008', name: 'Hailu Seyoum', status: 'Active' }
];

// Sample Enrollments (which trainees are in which batches)
const enrollments = [
    { traineeId: 1, batchId: 1 },
    { traineeId: 2, batchId: 1 },
    { traineeId: 3, batchId: 1 },
    { traineeId: 4, batchId: 1 },
    { traineeId: 5, batchId: 1 },
    { traineeId: 1, batchId: 4 },
    { traineeId: 6, batchId: 1 },
    { traineeId: 7, batchId: 1 },
    { traineeId: 8, batchId: 1 },
    { traineeId: 5, batchId: 3 },
    { traineeId: 6, batchId: 3 },
    { traineeId: 7, batchId: 3 },
    { traineeId: 1, batchId: 2 }
];

let attendanceData = {};

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    populateBatchSelect();
    populateSessionSelect();
    setupEventListeners();
    setDefaultDate();
});

// ============================================
// Setup Event Listeners
// ============================================
function setupEventListeners() {
    document.getElementById('saveAttendanceBtn').addEventListener('click', saveAttendance);
}

// ============================================
// Set Default Date
// ============================================
function setDefaultDate() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('attendanceDate').value = today;
}

// ============================================
// Populate Batch Select
// ============================================
function populateBatchSelect() {
    const select = document.getElementById('batchSelect');
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
// Populate Session Select
// ============================================
function populateSessionSelect() {
    const select = document.getElementById('sessionSelect');
    if (!select) return;
    
    select.innerHTML = '<option value="">Select Session</option>';
    sessions.forEach(session => {
        const batch = batches.find(b => b.id === session.batchId);
        const option = document.createElement('option');
        option.value = session.id;
        option.textContent = `${session.date} - ${session.topic} (${batch ? batch.name : 'N/A'})`;
        option.dataset.batchId = session.batchId;
        select.appendChild(option);
    });
}

// ============================================
// Load Trainees
// ============================================
function loadTrainees() {
    const batchId = parseInt(document.getElementById('batchSelect').value);
    const sessionId = parseInt(document.getElementById('sessionSelect').value);
    const tbody = document.getElementById('attendanceTableBody');
    const summaryRow = document.getElementById('summaryRow');
    
    if (!batchId || !sessionId) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4 text-muted">
                    <i class="fas fa-users fa-2x d-block mb-2"></i>
                    Select a batch and session to load trainees
                </td>
            </tr>
        `;
        summaryRow.style.display = 'none';
        document.getElementById('traineeCount').textContent = '0';
        return;
    }
    
    // Get enrolled trainees for this batch
    const enrolledTrainees = enrollments
        .filter(e => e.batchId === batchId)
        .map(e => trainees.find(t => t.id === e.traineeId))
        .filter(t => t && t.status === 'Active');
    
    if (enrolledTrainees.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center py-4 text-muted">
                    <i class="fas fa-user-slash fa-2x d-block mb-2"></i>
                    No trainees enrolled in this batch
                </td>
            </tr>
        `;
        summaryRow.style.display = 'none';
        document.getElementById('traineeCount').textContent = '0';
        return;
    }
    
    document.getElementById('traineeCount').textContent = enrolledTrainees.length;
    summaryRow.style.display = 'flex';
    
    // Initialize attendance data for this session
    if (!attendanceData[sessionId]) {
        attendanceData[sessionId] = {};
        enrolledTrainees.forEach(t => {
            attendanceData[sessionId][t.id] = 'Not Marked';
        });
    }
    
    // Render trainees
    let html = '';
    enrolledTrainees.forEach((trainee, index) => {
        const status = attendanceData[sessionId][trainee.id] || 'Not Marked';
        const initials = getInitials(trainee.name);
        
        html += `
            <tr>
                <td>${index + 1}</td>
                <td>
                    <div class="trainee-avatar">${initials}</div>
                </td>
                <td><strong>${trainee.name}</strong></td>
                <td><span class="text-muted small">${trainee.code}</span></td>
                <td>
                    <div class="attendance-status">
                        <div class="btn-group btn-group-sm" role="group">
                            <button type="button" class="btn btn-outline-success present ${status === 'Present' ? 'active-status' : ''}" 
                                    onclick="setStatus(${sessionId}, ${trainee.id}, 'Present')">
                                <i class="fas fa-check"></i>
                            </button>
                            <button type="button" class="btn btn-outline-danger absent ${status === 'Absent' ? 'active-status' : ''}" 
                                    onclick="setStatus(${sessionId}, ${trainee.id}, 'Absent')">
                                <i class="fas fa-times"></i>
                            </button>
                            <button type="button" class="btn btn-outline-warning late ${status === 'Late' ? 'active-status' : ''}" 
                                    onclick="setStatus(${sessionId}, ${trainee.id}, 'Late')">
                                <i class="fas fa-clock"></i>
                            </button>
                            <button type="button" class="btn btn-outline-info excused ${status === 'Excused' ? 'active-status' : ''}" 
                                    onclick="setStatus(${sessionId}, ${trainee.id}, 'Excused')">
                                <i class="fas fa-shield-alt"></i>
                            </button>
                        </div>
                    </div>
                </td>
                <td>
                    <input type="text" class="form-control form-control-sm" placeholder="Remarks..." 
                           id="remark_${sessionId}_${trainee.id}" style="max-width: 150px;">
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
    updateSummary(sessionId);
}

// ============================================
// Set Attendance Status
// ============================================
function setStatus(sessionId, traineeId, status) {
    if (!attendanceData[sessionId]) {
        attendanceData[sessionId] = {};
    }
    
    // Toggle off if same status clicked
    if (attendanceData[sessionId][traineeId] === status) {
        attendanceData[sessionId][traineeId] = 'Not Marked';
    } else {
        attendanceData[sessionId][traineeId] = status;
    }
    
    // Update UI
    const session = sessions.find(s => s.id === sessionId);
    if (session) {
        loadTrainees();
    }
}

// ============================================
// Mark All Present
// ============================================
function markAll(status) {
    const sessionId = parseInt(document.getElementById('sessionSelect').value);
    if (!sessionId) return;
    
    const batchId = parseInt(document.getElementById('batchSelect').value);
    if (!batchId) return;
    
    const enrolledTrainees = enrollments
        .filter(e => e.batchId === batchId)
        .map(e => trainees.find(t => t.id === e.traineeId))
        .filter(t => t && t.status === 'Active');
    
    if (!attendanceData[sessionId]) {
        attendanceData[sessionId] = {};
    }
    
    enrolledTrainees.forEach(t => {
        attendanceData[sessionId][t.id] = status;
    });
    
    loadTrainees();
    showAlert(`All trainees marked as ${status}`, 'success');
}

// ============================================
// Reset All
// ============================================
function resetAll() {
    const sessionId = parseInt(document.getElementById('sessionSelect').value);
    if (!sessionId) return;
    
    const batchId = parseInt(document.getElementById('batchSelect').value);
    if (!batchId) return;
    
    if (attendanceData[sessionId]) {
        delete attendanceData[sessionId];
    }
    
    loadTrainees();
    showAlert('All attendance reset', 'info');
}

// ============================================
// Update Summary
// ============================================
function updateSummary(sessionId) {
    if (!attendanceData[sessionId]) {
        document.getElementById('presentCount').textContent = '0';
        document.getElementById('absentCount').textContent = '0';
        document.getElementById('lateCount').textContent = '0';
        document.getElementById('excusedCount').textContent = '0';
        return;
    }
    
    const data = attendanceData[sessionId];
    let present = 0, absent = 0, late = 0, excused = 0;
    
    Object.values(data).forEach(status => {
        if (status === 'Present') present++;
        else if (status === 'Absent') absent++;
        else if (status === 'Late') late++;
        else if (status === 'Excused') excused++;
    });
    
    document.getElementById('presentCount').textContent = present;
    document.getElementById('absentCount').textContent = absent;
    document.getElementById('lateCount').textContent = late;
    document.getElementById('excusedCount').textContent = excused;
}

// ============================================
// Save Attendance
// ============================================
function saveAttendance() {
    const sessionId = parseInt(document.getElementById('sessionSelect').value);
    const batchId = parseInt(document.getElementById('batchSelect').value);
    const date = document.getElementById('attendanceDate').value;
    
    if (!sessionId || !batchId) {
        showAlert('Please select a batch and session', 'warning');
        return;
    }
    
    if (!attendanceData[sessionId]) {
        showAlert('No attendance data to save', 'warning');
        return;
    }
    
    // Get all enrolled trainees
    const enrolledTrainees = enrollments
        .filter(e => e.batchId === batchId)
        .map(e => trainees.find(t => t.id === e.traineeId))
        .filter(t => t && t.status === 'Active');
    
    // Check if all trainees have attendance marked
    const data = attendanceData[sessionId];
    let allMarked = true;
    let notMarked = [];
    
    enrolledTrainees.forEach(t => {
        if (!data[t.id] || data[t.id] === 'Not Marked') {
            allMarked = false;
            notMarked.push(t.name);
        }
    });
    
    if (!allMarked) {
        if (!confirm(`The following trainees have not been marked: ${notMarked.join(', ')}\n\nContinue anyway?`)) {
            return;
        }
    }
    
    // Collect remarks
    const attendance = [];
    enrolledTrainees.forEach(t => {
        const remarkInput = document.getElementById(`remark_${sessionId}_${t.id}`);
        const remark = remarkInput ? remarkInput.value.trim() : '';
        attendance.push({
            traineeId: t.id,
            traineeName: t.name,
            status: data[t.id] || 'Not Marked',
            remark: remark
        });
    });
    
    // Build attendance data for saving
    const attendanceDataToSave = {
        sessionId: sessionId,
        batchId: batchId,
        date: date,
        attendance: attendance
    };
    
    console.log('Saving attendance:', attendanceDataToSave);
    
    // Here you would send to backend API
    // For now, show success message
    showAlert('Attendance saved successfully!', 'success');
}

// ============================================
// Utility Functions
// ============================================
function getInitials(name) {
    if (!name) return 'U';
    return name.split(' ').map(word => word.charAt(0)).join('').toUpperCase().substring(0, 2);
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
    populateBatchSelect();
    populateSessionSelect();
    setDefaultDate();
});
