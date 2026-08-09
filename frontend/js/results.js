/* ============================================
   STTIMS - Results Management JavaScript
   ============================================ */

// Sample Data
const assessments = [
    { id: 1, title: 'Python Basics Quiz', batchId: 1, maxMarks: 20, passingMarks: 10 },
    { id: 2, title: 'Python Midterm Exam', batchId: 1, maxMarks: 50, passingMarks: 25 },
    { id: 3, title: 'Python Final Project', batchId: 1, maxMarks: 100, passingMarks: 50 },
    { id: 4, title: 'Safety Standards Quiz', batchId: 3, maxMarks: 20, passingMarks: 10 },
    { id: 5, title: 'Project Management Midterm', batchId: 4, maxMarks: 50, passingMarks: 25 }
];

const batches = [
    { id: 1, name: 'Python Batch 1' },
    { id: 2, name: 'Python Batch 2' },
    { id: 3, name: 'Electrical Safety Weekend' },
    { id: 4, name: 'Web Development PHP Batch 1' }
];

const trainees = [
    { id: 1, code: 'T-2024-001', name: 'Abebe Tesfaye' },
    { id: 2, code: 'T-2024-002', name: 'Birtukan Wolde' },
    { id: 3, code: 'T-2024-003', name: 'Chala Hailu' },
    { id: 4, code: 'T-2024-004', name: 'Desta Bekele' },
    { id: 5, code: 'T-2024-005', name: 'Emebet Girma' },
    { id: 6, code: 'T-2024-006', name: 'Fikre Ayele' },
    { id: 7, code: 'T-2024-007', name: 'Genet Assefa' },
    { id: 8, code: 'T-2024-008', name: 'Hailu Seyoum' }
];

const enrollments = [
    { traineeId: 1, batchId: 1 },
    { traineeId: 2, batchId: 1 },
    { traineeId: 3, batchId: 1 },
    { traineeId: 4, batchId: 1 },
    { traineeId: 5, batchId: 1 },
    { traineeId: 6, batchId: 1 },
    { traineeId: 7, batchId: 1 },
    { traineeId: 8, batchId: 1 },
    { traineeId: 5, batchId: 3 },
    { traineeId: 6, batchId: 3 },
    { traineeId: 7, batchId: 3 },
    { traineeId: 1, batchId: 4 }
];

// Grade Scale
const gradeScale = [
    { grade: 'A', min: 85, max: 100 },
    { grade: 'A-', min: 80, max: 84 },
    { grade: 'B+', min: 75, max: 79 },
    { grade: 'B', min: 70, max: 74 },
    { grade: 'B-', min: 65, max: 69 },
    { grade: 'C+', min: 60, max: 64 },
    { grade: 'C', min: 55, max: 59 },
    { grade: 'C-', min: 50, max: 54 },
    { grade: 'D', min: 45, max: 49 },
    { grade: 'F', min: 0, max: 44 }
];

// Sample Results Data
let results = {
    // assessmentId: { traineeId: { marks, percentage, grade, status, remarks } }
};

let currentAssessmentId = null;

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    populateAssessmentSelect();
    setupEventListeners();
});

// ============================================
// Setup Event Listeners
// ============================================
function setupEventListeners() {
    document.getElementById('saveResultsBtn').addEventListener('click', saveResults);
}

// ============================================
// Populate Assessment Select
// ============================================
function populateAssessmentSelect() {
    const select = document.getElementById('assessmentSelect');
    if (!select) return;
    
    select.innerHTML = '<option value="">Select Assessment</option>';
    assessments.forEach(assessment => {
        const batch = batches.find(b => b.id === assessment.batchId);
        const option = document.createElement('option');
        option.value = assessment.id;
        option.textContent = `${assessment.title} (${batch ? batch.name : 'N/A'})`;
        option.dataset.batchId = assessment.batchId;
        option.dataset.maxMarks = assessment.maxMarks;
        option.dataset.passingMarks = assessment.passingMarks;
        select.appendChild(option);
    });
}

// ============================================
// Load Trainees
// ============================================
function loadTrainees() {
    const assessmentId = parseInt(document.getElementById('assessmentSelect').value);
    const tbody = document.getElementById('resultsTableBody');
    const summaryRow = document.getElementById('summaryRow');
    const assessment = assessments.find(a => a.id === assessmentId);
    
    if (!assessmentId || !assessment) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center py-4 text-muted">
                    <i class="fas fa-chart-bar fa-2x d-block mb-2"></i>
                    Select an assessment to load trainees
                </td>
            </tr>
        `;
        summaryRow.style.display = 'none';
        document.getElementById('batchDisplay').value = '';
        document.getElementById('totalTrainees').textContent = '0 Trainees';
        document.getElementById('resultCount').textContent = '0';
        return;
    }
    
    currentAssessmentId = assessmentId;
    const batch = batches.find(b => b.id === assessment.batchId);
    document.getElementById('batchDisplay').value = batch ? batch.name : 'N/A';
    
    // Get enrolled trainees for this batch
    const enrolledTrainees = enrollments
        .filter(e => e.batchId === assessment.batchId)
        .map(e => trainees.find(t => t.id === e.traineeId))
        .filter(t => t);
    
    if (enrolledTrainees.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center py-4 text-muted">
                    <i class="fas fa-user-slash fa-2x d-block mb-2"></i>
                    No trainees enrolled in this batch
                </td>
            </tr>
        `;
        summaryRow.style.display = 'none';
        document.getElementById('totalTrainees').textContent = '0 Trainees';
        document.getElementById('resultCount').textContent = '0';
        return;
    }
    
    document.getElementById('totalTrainees').textContent = `${enrolledTrainees.length} Trainees`;
    document.getElementById('resultCount').textContent = enrolledTrainees.length;
    summaryRow.style.display = 'flex';
    
    // Initialize results for this assessment if not exists
    if (!results[assessmentId]) {
        results[assessmentId] = {};
        enrolledTrainees.forEach(t => {
            results[assessmentId][t.id] = {
                marks: null,
                percentage: null,
                grade: null,
                status: 'Not Attempted',
                remarks: ''
            };
        });
    }
    
    // Render trainees
    let html = '';
    let passCount = 0, failCount = 0, pendingCount = 0;
    let totalMarks = 0, marksCount = 0;
    
    enrolledTrainees.forEach((trainee, index) => {
        const result = results[assessmentId][trainee.id] || { 
            marks: null, percentage: null, grade: null, status: 'Not Attempted', remarks: '' 
        };
        const initials = getInitials(trainee.name);
        
        const statusClass = result.status === 'Pass' ? 'pass' : 
                           result.status === 'Fail' ? 'fail' : 'not-attempted';
        const statusDisplay = result.status || 'Not Attempted';
        
        if (result.status === 'Pass') passCount++;
        else if (result.status === 'Fail') failCount++;
        else pendingCount++;
        
        if (result.marks !== null && result.marks !== '') {
            totalMarks += parseFloat(result.marks);
            marksCount++;
        }
        
        const gradeClass = result.grade || 'Not Attempted';
        
        html += `
            <tr>
                <td>${index + 1}</td>
                <td>
                    <div class="trainee-avatar">${initials}</div>
                </td>
                <td><strong>${trainee.name}</strong></td>
                <td><span class="text-muted small">${trainee.code}</span></td>
                <td>
                    <input type="number" class="form-control form-control-sm marks-input" 
                           id="marks_${assessmentId}_${trainee.id}" 
                           value="${result.marks !== null ? result.marks : ''}"
                           min="0" max="${assessment.maxMarks}" 
                           step="0.5"
                           oninput="calculateResult(${assessmentId}, ${trainee.id})"
                           placeholder="0">
                </td>
                <td>
                    <span id="percentage_${assessmentId}_${trainee.id}">
                        ${result.percentage !== null ? result.percentage + '%' : '-'}
                    </span>
                </td>
                <td>
                    <span class="grade-badge ${gradeClass}" id="grade_${assessmentId}_${trainee.id}">
                        ${result.grade || '-'}
                    </span>
                </td>
                <td>
                    <span class="status-badge ${statusClass}" id="status_${assessmentId}_${trainee.id}">
                        ${statusDisplay}
                    </span>
                </td>
                <td>
                    <input type="text" class="form-control form-control-sm" 
                           id="remarks_${assessmentId}_${trainee.id}" 
                           value="${result.remarks || ''}"
                           placeholder="Remarks...">
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
    
    // Update summary
    document.getElementById('passCount').textContent = passCount;
    document.getElementById('failCount').textContent = failCount;
    document.getElementById('pendingCount').textContent = pendingCount;
    document.getElementById('avgMarks').textContent = marksCount > 0 ? 
        (totalMarks / marksCount).toFixed(1) : '0';
}

// ============================================
// Calculate Result
// ============================================
function calculateResult(assessmentId, traineeId) {
    const marksInput = document.getElementById(`marks_${assessmentId}_${traineeId}`);
    const marks = parseFloat(marksInput.value);
    const assessment = assessments.find(a => a.id === assessmentId);
    
    if (!assessment) return;
    
    const percentageEl = document.getElementById(`percentage_${assessmentId}_${traineeId}`);
    const gradeEl = document.getElementById(`grade_${assessmentId}_${traineeId}`);
    const statusEl = document.getElementById(`status_${assessmentId}_${traineeId}`);
    
    let percentage = null;
    let grade = null;
    let status = 'Not Attempted';
    
    if (marks !== null && !isNaN(marks) && marks >= 0) {
        percentage = (marks / assessment.maxMarks) * 100;
        percentage = Math.round(percentage * 100) / 100;
        
        // Determine grade
        for (const g of gradeScale) {
            if (percentage >= g.min && percentage <= g.max) {
                grade = g.grade;
                break;
            }
        }
        
        // Determine status
        const passingMarks = assessment.passingMarks || assessment.maxMarks * 0.5;
        status = marks >= passingMarks ? 'Pass' : 'Fail';
    } else if (marksInput.value === '' || marksInput.value === null) {
        status = 'Not Attempted';
    }
    
    // Update display
    percentageEl.textContent = percentage !== null ? percentage + '%' : '-';
    gradeEl.textContent = grade || '-';
    gradeEl.className = `grade-badge ${grade || 'Not Attempted'}`;
    statusEl.textContent = status;
    statusEl.className = `status-badge ${status === 'Pass' ? 'pass' : status === 'Fail' ? 'fail' : 'not-attempted'}`;
    
    // Store result
    if (!results[assessmentId]) {
        results[assessmentId] = {};
    }
    if (!results[assessmentId][traineeId]) {
        results[assessmentId][traineeId] = { marks: null, percentage: null, grade: null, status: 'Not Attempted', remarks: '' };
    }
    
    results[assessmentId][traineeId].marks = marks;
    results[assessmentId][traineeId].percentage = percentage;
    results[assessmentId][traineeId].grade = grade;
    results[assessmentId][traineeId].status = status;
    
    // Update summary
    updateSummary(assessmentId);
}

// ============================================
// Update Summary
// ============================================
function updateSummary(assessmentId) {
    if (!results[assessmentId]) return;
    
    const data = results[assessmentId];
    let passCount = 0, failCount = 0, pendingCount = 0;
    let totalMarks = 0, marksCount = 0;
    
    Object.values(data).forEach(result => {
        if (result.status === 'Pass') passCount++;
        else if (result.status === 'Fail') failCount++;
        else pendingCount++;
        
        if (result.marks !== null && result.marks !== '') {
            totalMarks += parseFloat(result.marks);
            marksCount++;
        }
    });
    
    document.getElementById('passCount').textContent = passCount;
    document.getElementById('failCount').textContent = failCount;
    document.getElementById('pendingCount').textContent = pendingCount;
    document.getElementById('avgMarks').textContent = marksCount > 0 ? 
        (totalMarks / marksCount).toFixed(1) : '0';
}

// ============================================
// Auto Fill Marks
// ============================================
function autoFillMarks() {
    const assessmentId = currentAssessmentId;
    if (!assessmentId) {
        showAlert('Please select an assessment first', 'warning');
        return;
    }
    
    const assessment = assessments.find(a => a.id === assessmentId);
    if (!assessment) return;
    
    const enrolledTrainees = enrollments
        .filter(e => e.batchId === assessment.batchId)
        .map(e => trainees.find(t => t.id === e.traineeId))
        .filter(t => t);
    
    // Fill with random marks for demo purposes
    enrolledTrainees.forEach(trainee => {
        const marksInput = document.getElementById(`marks_${assessmentId}_${trainee.id}`);
        if (marksInput) {
            const randomMarks = Math.round((Math.random() * assessment.maxMarks) * 2) / 2;
            marksInput.value = Math.min(randomMarks, assessment.maxMarks);
            calculateResult(assessmentId, trainee.id);
        }
    });
    
    showAlert('Auto-filled marks for all trainees', 'info');
}

// ============================================
// Reset All Marks
// ============================================
function resetAllMarks() {
    const assessmentId = currentAssessmentId;
    if (!assessmentId) {
        showAlert('Please select an assessment first', 'warning');
        return;
    }
    
    if (!confirm('Are you sure you want to reset all marks for this assessment?')) {
        return;
    }
    
    const enrolledTrainees = enrollments
        .filter(e => e.batchId === assessments.find(a => a.id === assessmentId).batchId)
        .map(e => trainees.find(t => t.id === e.traineeId))
        .filter(t => t);
    
    enrolledTrainees.forEach(trainee => {
        const marksInput = document.getElementById(`marks_${assessmentId}_${trainee.id}`);
        if (marksInput) {
            marksInput.value = '';
            calculateResult(assessmentId, trainee.id);
        }
    });
    
    results[assessmentId] = {};
    enrolledTrainees.forEach(t => {
        results[assessmentId][t.id] = {
            marks: null,
            percentage: null,
            grade: null,
            status: 'Not Attempted',
            remarks: ''
        };
    });
    
    updateSummary(assessmentId);
    showAlert('All marks reset successfully', 'success');
}

// ============================================
// Save Results
// ============================================
function saveResults() {
    const assessmentId = currentAssessmentId;
    if (!assessmentId) {
        showAlert('Please select an assessment first', 'warning');
        return;
    }
    
    const assessment = assessments.find(a => a.id === assessmentId);
    if (!assessment) return;
    
    // Collect all results with remarks
    const resultsData = [];
    const enrolledTrainees = enrollments
        .filter(e => e.batchId === assessment.batchId)
        .map(e => trainees.find(t => t.id === e.traineeId))
        .filter(t => t);
    
    let hasData = false;
    let allMarked = true;
    let notMarked = [];
    
    enrolledTrainees.forEach(trainee => {
        const marksInput = document.getElementById(`marks_${assessmentId}_${trainee.id}`);
        const remarksInput = document.getElementById(`remarks_${assessmentId}_${trainee.id}`);
        const result = results[assessmentId]?.[trainee.id];
        
        const marks = marksInput ? parseFloat(marksInput.value) : null;
        const remarks = remarksInput ? remarksInput.value.trim() : '';
        
        if (marks !== null && !isNaN(marks)) {
            hasData = true;
        } else {
            allMarked = false;
            notMarked.push(trainee.name);
        }
        
        resultsData.push({
            traineeId: trainee.id,
            traineeName: trainee.name,
            traineeCode: trainee.code,
            marks: marks,
            percentage: result?.percentage || null,
            grade: result?.grade || null,
            status: result?.status || 'Not Attempted',
            remarks: remarks
        });
    });
    
    if (!hasData) {
        showAlert('No marks entered to save', 'warning');
        return;
    }
    
    if (!allMarked) {
        if (!confirm(`The following trainees have not been marked: ${notMarked.join(', ')}\n\nContinue anyway?`)) {
            return;
        }
    }
    
    // Build results data for saving
    const resultsToSave = {
        assessmentId: assessmentId,
        assessmentTitle: assessment.title,
        batchId: assessment.batchId,
        maxMarks: assessment.maxMarks,
        passingMarks: assessment.passingMarks,
        results: resultsData,
        savedAt: new Date().toISOString()
    };
    
    console.log('Saving results:', resultsToSave);
    
    // Here you would send to backend API
    // For now, show success message
    showAlert('Results saved successfully!', 'success');
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
    populateAssessmentSelect();
});
