/* ============================================
   STTIMS - Reports JavaScript
   ============================================ */

// Sample Data for Reports
const reportData = {
    enrollment: {
        title: 'Enrollment Report',
        subtitle: 'Course enrollment statistics by course and batch',
        summary: [
            { label: 'Total Enrollments', value: 156 },
            { label: 'Active Enrollments', value: 98 },
            { label: 'Completed', value: 42 },
            { label: 'Dropped', value: 16 }
        ],
        chartData: {
            labels: ['Python', 'Electrical Safety', 'Web Development', 'Project Management', 'Machine Learning'],
            datasets: [{
                label: 'Enrollments',
                data: [45, 28, 32, 35, 16],
                backgroundColor: ['#4F46E5', '#10B981', '#F59E0B', '#EF4444', '#7C3AED']
            }]
        },
        tableData: [
            { course: 'Python Programming', batch: 'Batch 1', enrolled: 25, active: 18, completed: 5, dropped: 2 },
            { course: 'Python Programming', batch: 'Batch 2', enrolled: 20, active: 12, completed: 6, dropped: 2 },
            { course: 'Electrical Safety', batch: 'Weekend', enrolled: 28, active: 22, completed: 4, dropped: 2 },
            { course: 'Web Development', batch: 'Batch 1', enrolled: 32, active: 20, completed: 10, dropped: 2 },
            { course: 'Project Management', batch: 'Batch 1', enrolled: 35, active: 18, completed: 15, dropped: 2 },
            { course: 'Machine Learning', batch: 'Batch 1', enrolled: 16, active: 8, completed: 2, dropped: 6 }
        ]
    },
    attendance: {
        title: 'Attendance Report',
        subtitle: 'Session attendance tracking by batch',
        summary: [
            { label: 'Total Sessions', value: 284 },
            { label: 'Total Attendance Records', value: 1284 },
            { label: 'Average Attendance', value: '87%' },
            { label: 'Overall Pass Rate', value: '92%' }
        ],
        chartData: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
                { label: 'Present', data: [85, 78, 92, 88, 76, 45, 30], backgroundColor: '#10B981' },
                { label: 'Absent', data: [15, 22, 8, 12, 24, 15, 10], backgroundColor: '#EF4444' },
                { label: 'Late', data: [5, 8, 10, 6, 12, 8, 5], backgroundColor: '#F59E0B' }
            ]
        },
        tableData: [
            { batch: 'Python Batch 1', session: 'Session 1', date: '2024-02-01', present: 22, absent: 2, late: 1, rate: '88%' },
            { batch: 'Python Batch 1', session: 'Session 2', date: '2024-02-03', present: 20, absent: 3, late: 2, rate: '80%' },
            { batch: 'Electrical Safety', session: 'Session 1', date: '2024-02-17', present: 24, absent: 1, late: 0, rate: '96%' },
            { batch: 'Web Development', session: 'Session 1', date: '2024-03-01', present: 18, absent: 4, late: 2, rate: '72%' }
        ]
    },
    assessment: {
        title: 'Assessment Report',
        subtitle: 'Assessment results summary by assessment',
        summary: [
            { label: 'Total Assessments', value: 45 },
            { label: 'Completed', value: 28 },
            { label: 'Scheduled', value: 12 },
            { label: 'Cancelled', value: 5 }
        ],
        chartData: {
            labels: ['Quiz', 'Midterm', 'Final', 'Practical', 'Project', 'Assignment'],
            datasets: [{
                label: 'Results',
                data: [85, 72, 68, 90, 75, 80],
                backgroundColor: ['#4F46E5', '#10B981', '#F59E0B', '#EF4444', '#7C3AED', '#EC4899']
            }]
        },
        tableData: [
            { assessment: 'Python Basics Quiz', type: 'Quiz', maxMarks: 20, avgMarks: 16.5, passRate: '85%' },
            { assessment: 'Python Midterm', type: 'Exam', maxMarks: 50, avgMarks: 38.2, passRate: '72%' },
            { assessment: 'Python Final Project', type: 'Project', maxMarks: 100, avgMarks: 82.5, passRate: '90%' },
            { assessment: 'Safety Quiz', type: 'Quiz', maxMarks: 20, avgMarks: 17.0, passRate: '88%' }
        ]
    },
    revenue: {
        title: 'Revenue Report',
        subtitle: 'Financial revenue summary by course',
        summary: [
            { label: 'Total Revenue', value: 'ETB 2,450,000' },
            { label: 'Collected', value: 'ETB 1,850,000' },
            { label: 'Pending', value: 'ETB 600,000' },
            { label: 'Discounts Given', value: 'ETB 85,000' }
        ],
        chartData: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [
                { label: 'Revenue', data: [120000, 150000, 180000, 220000, 200000, 250000, 180000, 210000, 190000, 230000, 270000, 250000], borderColor: '#4F46E5', backgroundColor: 'rgba(79,70,229,0.1)' }
            ]
        },
        tableData: [
            { course: 'Python Programming', enrolled: 45, revenue: 'ETB 112,500', collected: 'ETB 98,000', pending: 'ETB 14,500' },
            { course: 'Electrical Safety', enrolled: 28, revenue: 'ETB 50,400', collected: 'ETB 42,000', pending: 'ETB 8,400' },
            { course: 'Web Development', enrolled: 32, revenue: 'ETB 112,000', collected: 'ETB 95,000', pending: 'ETB 17,000' },
            { course: 'Project Management', enrolled: 35, revenue: 'ETB 70,000', collected: 'ETB 58,000', pending: 'ETB 12,000' }
        ]
    },
    certificate: {
        title: 'Certificate Report',
        subtitle: 'Certificate issuance summary by course',
        summary: [
            { label: 'Total Issued', value: 892 },
            { label: 'Active', value: 750 },
            { label: 'Expired', value: 120 },
            { label: 'Revoked', value: 22 }
        ],
        chartData: {
            labels: ['Python', 'Electrical', 'Web Dev', 'Project Mgmt', 'Machine Learning'],
            datasets: [{
                label: 'Certificates Issued',
                data: [250, 180, 200, 150, 112],
                backgroundColor: ['#4F46E5', '#10B981', '#F59E0B', '#EF4444', '#7C3AED']
            }]
        },
        tableData: [
            { course: 'Python Programming', issued: 250, active: 210, expired: 30, revoked: 10 },
            { course: 'Electrical Safety', issued: 180, active: 160, expired: 15, revoked: 5 },
            { course: 'Web Development', issued: 200, active: 170, expired: 25, revoked: 5 },
            { course: 'Project Management', issued: 150, active: 130, expired: 15, revoked: 5 }
        ]
    },
    instructor: {
        title: 'Instructor Report',
        subtitle: 'Instructor workload and performance summary',
        summary: [
            { label: 'Total Instructors', value: 12 },
            { label: 'Active', value: 10 },
            { label: 'On Leave', value: 2 },
            { label: 'Avg Workload', value: '28 hrs' }
        ],
        chartData: {
            labels: ['Dr. Abebe', 'Dr. Tigist', 'Eng. Chalachew', 'Ms. Kidist', 'Dr. Yonas'],
            datasets: [{
                label: 'Teaching Hours',
                data: [40, 35, 30, 25, 20],
                backgroundColor: ['#4F46E5', '#10B981', '#F59E0B', '#EF4444', '#7C3AED']
            }]
        },
        tableData: [
            { instructor: 'Dr. Abebe Teshome', department: 'IT', batches: 3, trainees: 45, hours: 40 },
            { instructor: 'Dr. Tigist Wolde', department: 'Electrical', batches: 2, trainees: 28, hours: 35 },
            { instructor: 'Eng. Chalachew Assefa', department: 'Software', batches: 2, trainees: 32, hours: 30 },
            { instructor: 'Ms. Kidist Tadesse', department: 'Business', batches: 2, trainees: 35, hours: 25 }
        ]
    }
};

let currentReportType = 'enrollment';
let currentViewType = 'summary';
let chartInstance = null;

// ============================================
// Initialization
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    // Load default report
    loadReport('enrollment');
});

// ============================================
// Load Report
// ============================================
function loadReport(type) {
    currentReportType = type;
    const data = reportData[type];
    if (!data) return;
    
    // Update report title
    document.getElementById('reportTitle').textContent = data.title;
    document.getElementById('reportSubtitle').textContent = data.subtitle;
    document.getElementById('reportActions').style.display = 'flex';
    document.getElementById('reportTypeSelector').style.display = 'flex';
    
    // Highlight active report card
    document.querySelectorAll('.report-card').forEach(card => {
        card.style.border = 'none';
    });
    // Find and highlight the clicked card
    const cards = document.querySelectorAll('.report-card');
    const index = ['enrollment', 'attendance', 'assessment', 'revenue', 'certificate', 'instructor'].indexOf(type);
    if (index !== -1 && cards[index]) {
        cards[index].style.border = '2px solid #4F46E5';
    }
    
    // Render report
    renderReport(type, currentViewType);
}

// ============================================
// Switch Report Type
// ============================================
function switchReportType(type) {
    currentViewType = type;
    
    // Update active button
    document.querySelectorAll('.report-type-selector .btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`.report-type-selector .btn[data-type="${type}"]`).classList.add('active');
    
    renderReport(currentReportType, type);
}

// ============================================
// Render Report
// ============================================
function renderReport(type, viewType) {
    const data = reportData[type];
    if (!data) return;
    
    const container = document.getElementById('reportContent');
    let html = '';
    
    // Summary Section
    if (viewType === 'summary' || viewType === 'all') {
        html += `
            <div class="report-summary">
                ${data.summary.map(item => `
                    <div class="summary-item">
                        <div class="value">${item.value}</div>
                        <div class="label">${item.label}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    // Chart Section
    if (viewType === 'chart' || viewType === 'all') {
        html += `
            <div class="chart-container">
                <canvas id="reportChart"></canvas>
            </div>
        `;
    }
    
    // Table Section
    if (viewType === 'details' || viewType === 'all') {
        if (data.tableData && data.tableData.length > 0) {
            const headers = Object.keys(data.tableData[0]);
            html += `
                <div class="report-table-container">
                    <table class="table table-striped table-hover">
                        <thead>
                            <tr>
                                ${headers.map(h => `<th>${h.replace(/_/g, ' ').toUpperCase()}</th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            ${data.tableData.map(row => `
                                <tr>
                                    ${headers.map(h => `<td>${row[h] || '-'}</td>`).join('')}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        }
    }
    
    container.innerHTML = html;
    
    // Render chart if needed
    if (viewType === 'chart' || viewType === 'all') {
        renderChart(data.chartData);
    }
}

// ============================================
// Render Chart
// ============================================
function renderChart(chartData) {
    const canvas = document.getElementById('reportChart');
    if (!canvas) return;
    
    // Destroy existing chart
    if (chartInstance) {
        chartInstance.destroy();
    }
    
    const isPieChart = chartData.datasets.length === 1 && chartData.datasets[0].backgroundColor;
    
    chartInstance = new Chart(canvas, {
        type: isPieChart ? 'doughnut' : 'bar',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                }
            },
            scales: isPieChart ? undefined : {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// ============================================
// Export Functions
// ============================================
function exportPDF() {
    const element = document.getElementById('reportContent');
    const data = reportData[currentReportType];
    
    // Build PDF content
    let html = `
        <html>
            <head>
                <title>${data.title}</title>
                <style>
                    body { font-family: 'Inter', sans-serif; padding: 2rem; }
                    h1 { color: #1F2937; }
                    .summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.5rem 0; }
                    .summary-item { text-align: center; padding: 1rem; background: #f8fafc; border-radius: 8px; }
                    .summary-item .value { font-size: 1.25rem; font-weight: 700; }
                    .summary-item .label { font-size: 0.7rem; color: #6B7280; text-transform: uppercase; }
                    table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; }
                    th { background: #f8fafc; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; padding: 0.5rem; text-align: left; border: 1px solid #e5e7eb; }
                    td { padding: 0.5rem; border: 1px solid #e5e7eb; }
                    .footer { margin-top: 2rem; color: #6B7280; font-size: 0.75rem; text-align: center; }
                </style>
            </head>
            <body>
                <h1>${data.title}</h1>
                <p>${data.subtitle}</p>
                <div class="summary">
                    ${data.summary.map(item => `
                        <div class="summary-item">
                            <div class="value">${item.value}</div>
                            <div class="label">${item.label}</div>
                        </div>
                    `).join('')}
                </div>
                ${data.tableData && data.tableData.length > 0 ? `
                    <table>
                        <thead>
                            <tr>
                                ${Object.keys(data.tableData[0]).map(h => `<th>${h.replace(/_/g, ' ').toUpperCase()}</th>`).join('')}
                            </tr>
                        </thead>
                        <tbody>
                            ${data.tableData.map(row => `
                                <tr>
                                    ${Object.values(row).map(v => `<td>${v || '-'}</td>`).join('')}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                ` : ''}
                <div class="footer">
                    Generated on ${new Date().toLocaleString()} | STTIMS Reports
                </div>
            </body>
        </html>
    `;
    
    // Create print window for PDF
    const printWindow = window.open('', '_blank');
    printWindow.document.write(html);
    printWindow.document.close();
    
    setTimeout(() => {
        printWindow.print();
        // After print, close the window after user confirms
        setTimeout(() => {
            printWindow.close();
        }, 1000);
    }, 500);
}

function exportExcel() {
    const data = reportData[currentReportType];
    if (!data.tableData || data.tableData.length === 0) {
        showAlert('No data available to export', 'warning');
        return;
    }
    
    const headers = Object.keys(data.tableData[0]);
    let csv = headers.join(',') + '\n';
    data.tableData.forEach(row => {
        csv += headers.map(h => `"${row[h] || ''}"`).join(',') + '\n';
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentReportType}_report_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
    
    showAlert('Excel report downloaded successfully!', 'success');
}

function printReport() {
    const data = reportData[currentReportType];
    const content = document.getElementById('reportContent').innerHTML;
    
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>${data.title}</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body { padding: 2rem; font-family: 'Inter', sans-serif; }
                    .report-summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1.5rem 0; }
                    .report-summary .summary-item { text-align: center; padding: 1rem; background: #f8fafc; border-radius: 8px; }
                    .report-summary .summary-item .value { font-size: 1.25rem; font-weight: 700; }
                    .report-summary .summary-item .label { font-size: 0.7rem; color: #6B7280; text-transform: uppercase; }
                    .report-table-container { margin: 1.5rem 0; }
                    table { width: 100%; border-collapse: collapse; }
                    th { background: #f8fafc; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; padding: 0.5rem; text-align: left; border: 1px solid #e5e7eb; }
                    td { padding: 0.5rem; border: 1px solid #e5e7eb; }
                    .footer { margin-top: 2rem; color: #6B7280; font-size: 0.75rem; text-align: center; }
                    .no-print { display: none; }
                </style>
            </head>
            <body>
                <h2>${data.title}</h2>
                <p>${data.subtitle}</p>
                ${content}
                <div class="footer">
                    Generated on ${new Date().toLocaleString()} | STTIMS Reports
                </div>
                <div class="text-center mt-4 no-print">
                    <button class="btn btn-primary" onclick="window.print()">Print</button>
                    <button class="btn btn-secondary" onclick="window.close()">Close</button>
                </div>
            </body>
        </html>
    `);
    printWindow.document.close();
}

// ============================================
// Utility Functions
// ============================================
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
    // Load enrollment report by default
    loadReport('enrollment');
});
