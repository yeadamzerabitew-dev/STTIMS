/**
 * Dashboard - API Version
 */

import { UserAPI, TraineeAPI, InstructorAPI, CourseAPI, BatchAPI, EnrollmentAPI } from './api.js';

async function loadDashboard() {
    try {
        const [users, trainees, instructors, courses, batches, enrollments] = await Promise.all([
            UserAPI.getAll(),
            TraineeAPI.getAll(),
            InstructorAPI.getAll(),
            CourseAPI.getAll(),
            BatchAPI.getAll(),
            EnrollmentAPI.getAll()
        ]);
        
        const stats = {
            users: users.data?.length || 0,
            trainees: trainees.data?.length || 0,
            instructors: instructors.data?.length || 0,
            courses: courses.data?.length || 0,
            batches: batches.data?.length || 0,
            enrollments: enrollments.data?.length || 0
        };
        
        updateStats(stats);
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showAlert('Error loading dashboard data', 'danger');
    }
}

function updateStats(stats) {
    const elements = {
        'totalUsers': stats.users,
        'totalTrainees': stats.trainees,
        'totalInstructors': stats.instructors,
        'totalCourses': stats.courses,
        'totalBatches': stats.batches,
        'totalEnrollments': stats.enrollments
    };
    
    Object.entries(elements).forEach(([id, value]) => {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    });
}

function showAlert(message, type) {
    const container = document.getElementById('alertContainer');
    if (!container) return;
    container.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => container.innerHTML = '', 3000);
}

document.addEventListener('DOMContentLoaded', loadDashboard);
