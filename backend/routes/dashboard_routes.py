from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import (
    db, User, Trainee, Instructor, Course, Category, Batch, Enrollment,
    Certificate, CourseAssignment, ClassSession, AttendanceRecord
)
from datetime import datetime, timedelta
from sqlalchemy import func
from utils.decorators import require_module

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


# =============================================
# SCOPE HELPERS
# =============================================

def _instructor_batch_ids():
    """Batch IDs the current instructor has ever been assigned to teach."""
    if not current_user.instructor_id:
        return []
    rows = db.session.query(CourseAssignment.batch_id).filter(
        CourseAssignment.instructor_id == current_user.instructor_id
    ).distinct().all()
    return [r[0] for r in rows]


# =============================================
# STATS  (GET /api/dashboard/stats)
# =============================================

def _admin_manager_stats():
    total_trainees = Trainee.query.filter_by(status='Active').count()
    active_instructors = Instructor.query.filter_by(status='Active').count()
    active_courses = Course.query.filter_by(status='Active').count()
    certificates_issued = Certificate.query.filter_by(status='Issued').count()
    total_batches = Batch.query.count()
    active_enrollments = Enrollment.query.filter_by(status='Active').count()

    upcoming_sessions = Batch.query.filter(
        Batch.start_date > datetime.now().date(),
        Batch.status == 'Upcoming'
    ).count()

    total_enrollments = Enrollment.query.count()
    completed_enrollments = Enrollment.query.filter_by(status='Completed').count()
    completion_rate = round((completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0, 1)

    today = datetime.now().date()
    today_registrations = Enrollment.query.filter(
        func.date(Enrollment.enrollment_date) == today
    ).count()

    pending_certificates = Certificate.query.filter_by(status='Pending').count()

    upcoming_deadlines = 0
    if hasattr(Enrollment, 'completion_date'):
        upcoming_deadlines = Enrollment.query.filter(
            func.date(Enrollment.completion_date) >= today,
            func.date(Enrollment.completion_date) <= today + timedelta(days=7),
            Enrollment.status == 'Active'
        ).count()

    total_revenue = db.session.query(func.sum(Enrollment.final_amount)).filter(
        Enrollment.payment_status == 'Paid'
    ).scalar() or 0
    pending_revenue = db.session.query(func.sum(Enrollment.final_amount)).filter(
        Enrollment.payment_status.in_(['Pending', 'Partial'])
    ).scalar() or 0

    return {
        'labels': {
            'card1': 'Total Trainees', 'card2': 'Active Instructors',
            'card3': 'Active Courses', 'card4': 'Certificates Issued',
            'card5': 'Total Batches', 'card6': 'Active Enrollments',
            'card7': 'Upcoming Sessions', 'card8': 'Completion Rate'
        },
        'total_trainees': total_trainees,
        'active_instructors': active_instructors,
        'active_courses': active_courses,
        'certificates_issued': certificates_issued,
        'total_batches': total_batches,
        'active_enrollments': active_enrollments,
        'upcoming_sessions': upcoming_sessions,
        'completion_rate': completion_rate,
        'today_registrations': today_registrations,
        'pending_certificates': pending_certificates,
        'upcoming_deadlines': upcoming_deadlines,
        'total_revenue': float(total_revenue),
        'pending_revenue': float(pending_revenue)
    }


def _instructor_stats():
    labels = {
        'card1': 'My Trainees', 'card2': 'My Active Batches',
        'card3': 'My Courses', 'card4': 'Certificates Issued',
        'card5': 'My Total Batches', 'card6': 'My Active Enrollments',
        'card7': 'My Upcoming Sessions', 'card8': 'My Completion Rate'
    }
    batch_ids = _instructor_batch_ids()
    today = datetime.now().date()

    if not batch_ids:
        return {
            'labels': labels,
            'total_trainees': 0, 'active_instructors': 0, 'active_courses': 0,
            'certificates_issued': 0, 'total_batches': 0, 'active_enrollments': 0,
            'upcoming_sessions': 0, 'completion_rate': 0, 'today_registrations': 0,
            'pending_certificates': 0, 'upcoming_deadlines': 0,
            'total_revenue': 0, 'pending_revenue': 0
        }

    my_trainees = db.session.query(Enrollment.trainee_id).filter(
        Enrollment.batch_id.in_(batch_ids)
    ).distinct().count()

    my_courses = db.session.query(Batch.course_id).filter(
        Batch.batch_id.in_(batch_ids)
    ).distinct().count()

    active_batches = Batch.query.filter(
        Batch.batch_id.in_(batch_ids),
        Batch.status.in_(['Upcoming', 'Ongoing'])
    ).count()

    active_enrollments = Enrollment.query.filter(
        Enrollment.batch_id.in_(batch_ids),
        Enrollment.status == 'Active'
    ).count()

    upcoming_sessions = ClassSession.query.filter(
        ClassSession.instructor_id == current_user.instructor_id,
        ClassSession.session_date >= today,
        ClassSession.status == 'Scheduled'
    ).count()

    total_enr = Enrollment.query.filter(Enrollment.batch_id.in_(batch_ids)).count()
    completed_enr = Enrollment.query.filter(
        Enrollment.batch_id.in_(batch_ids), Enrollment.status == 'Completed'
    ).count()
    completion_rate = round((completed_enr / total_enr * 100) if total_enr > 0 else 0, 1)

    certs = Certificate.query.join(Enrollment).filter(
        Enrollment.batch_id.in_(batch_ids),
        Certificate.status == 'Issued'
    ).count()

    today_registrations = Enrollment.query.filter(
        Enrollment.batch_id.in_(batch_ids),
        func.date(Enrollment.enrollment_date) == today
    ).count()

    pending_certificates = Certificate.query.join(Enrollment).filter(
        Enrollment.batch_id.in_(batch_ids),
        Certificate.status == 'Pending'
    ).count()

    upcoming_deadlines = 0
    if hasattr(Enrollment, 'completion_date'):
        upcoming_deadlines = Enrollment.query.filter(
            Enrollment.batch_id.in_(batch_ids),
            func.date(Enrollment.completion_date) >= today,
            func.date(Enrollment.completion_date) <= today + timedelta(days=7),
            Enrollment.status == 'Active'
        ).count()

    return {
        'labels': labels,
        'total_trainees': my_trainees,
        'active_instructors': active_batches,
        'active_courses': my_courses,
        'certificates_issued': certs,
        'total_batches': len(batch_ids),
        'active_enrollments': active_enrollments,
        'upcoming_sessions': upcoming_sessions,
        'completion_rate': completion_rate,
        'today_registrations': today_registrations,
        'pending_certificates': pending_certificates,
        'upcoming_deadlines': upcoming_deadlines,
        'total_revenue': 0,
        'pending_revenue': 0
    }


def _trainee_stats():
    labels = {
        'card1': 'My Batches', 'card2': 'My Instructors',
        'card3': 'My Courses', 'card4': 'My Certificates',
        'card5': 'My Enrollments', 'card6': 'My Active Enrollments',
        'card7': 'My Upcoming Sessions', 'card8': 'My Completion Rate'
    }

    if not current_user.trainee_id:
        return {
            'labels': labels,
            'total_trainees': 0, 'active_instructors': 0, 'active_courses': 0,
            'certificates_issued': 0, 'total_batches': 0, 'active_enrollments': 0,
            'upcoming_sessions': 0, 'completion_rate': 0, 'today_registrations': 0,
            'pending_certificates': 0, 'upcoming_deadlines': 0,
            'total_revenue': 0, 'pending_revenue': 0
        }

    today = datetime.now().date()
    enrollments = Enrollment.query.filter_by(trainee_id=current_user.trainee_id).all()
    batch_ids = list({e.batch_id for e in enrollments})

    my_courses = db.session.query(Batch.course_id).filter(
        Batch.batch_id.in_(batch_ids)
    ).distinct().count() if batch_ids else 0

    my_instructors = db.session.query(CourseAssignment.instructor_id).filter(
        CourseAssignment.batch_id.in_(batch_ids)
    ).distinct().count() if batch_ids else 0

    active_enrollments = len([e for e in enrollments if e.status == 'Active'])

    upcoming_sessions = ClassSession.query.filter(
        ClassSession.batch_id.in_(batch_ids),
        ClassSession.session_date >= today,
        ClassSession.status == 'Scheduled'
    ).count() if batch_ids else 0

    my_certificates = Certificate.query.join(Enrollment).filter(
        Enrollment.trainee_id == current_user.trainee_id,
        Certificate.status == 'Issued'
    ).count()

    total_enr = len(enrollments)
    completed_enr = len([e for e in enrollments if e.status == 'Completed'])
    completion_rate = round((completed_enr / total_enr * 100) if total_enr > 0 else 0, 1)

    pending_certificates = Certificate.query.join(Enrollment).filter(
        Enrollment.trainee_id == current_user.trainee_id,
        Certificate.status == 'Pending'
    ).count()

    upcoming_deadlines = 0
    if hasattr(Enrollment, 'completion_date'):
        upcoming_deadlines = len([
            e for e in enrollments
            if e.status == 'Active' and e.completion_date
            and today <= e.completion_date <= today + timedelta(days=7)
        ])

    return {
        'labels': labels,
        'total_trainees': len(batch_ids),
        'active_instructors': my_instructors,
        'active_courses': my_courses,
        'certificates_issued': my_certificates,
        'total_batches': total_enr,
        'active_enrollments': active_enrollments,
        'upcoming_sessions': upcoming_sessions,
        'completion_rate': completion_rate,
        'today_registrations': 0,
        'pending_certificates': pending_certificates,
        'upcoming_deadlines': upcoming_deadlines,
        'total_revenue': 0,
        'pending_revenue': 0
    }


@dashboard_bp.route('/stats', methods=['GET'])
@login_required
@require_module('dashboard')
def get_stats():
    """Dashboard statistics, scoped to the logged-in user's role."""
    try:
        if current_user.role in ('Admin', 'Manager'):
            data = _admin_manager_stats()
        elif current_user.role == 'Instructor':
            data = _instructor_stats()
        elif current_user.role == 'Trainee':
            data = _trainee_stats()
        else:
            data = _admin_manager_stats()

        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@dashboard_bp.route('/overview', methods=['GET'])
@login_required
@require_module('dashboard')
def get_overview():
    """Get dashboard overview data (Admin/Manager only - global counts)"""
    try:
        return jsonify({
            'success': True,
            'data': {
                'total_users': User.query.count(),
                'total_trainees': Trainee.query.count(),
                'total_instructors': Instructor.query.count(),
                'total_courses': Course.query.count(),
                'total_batches': Batch.query.count(),
                'total_enrollments': Enrollment.query.count()
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# =============================================
# ENROLLMENT TRENDS  (feeds "Course Enrollment Trends" chart)
# =============================================

@dashboard_bp.route('/enrollment-trends', methods=['GET'])
@login_required
@require_module('dashboard')
def get_enrollment_trends():
    """Monthly enrollment counts for the last 7 months, scoped to the user's role."""
    try:
        months = []
        counts = []
        today = datetime.now().date()

        if current_user.role in ('Admin', 'Manager'):
            batch_filter = None
        elif current_user.role == 'Instructor':
            batch_filter = _instructor_batch_ids()
        elif current_user.role == 'Trainee':
            if current_user.trainee_id:
                batch_filter = [
                    r[0] for r in db.session.query(Enrollment.batch_id).filter(
                        Enrollment.trainee_id == current_user.trainee_id
                    ).distinct().all()
                ]
            else:
                batch_filter = []
        else:
            batch_filter = None

        for i in range(6, -1, -1):
            month_date = today.replace(day=1) - timedelta(days=i * 30)
            month_start = month_date.replace(day=1)

            if month_start.month == 12:
                next_month = month_start.replace(year=month_start.year + 1, month=1, day=1)
            else:
                next_month = month_start.replace(month=month_start.month + 1, day=1)

            query = Enrollment.query.filter(
                Enrollment.enrollment_date >= month_start,
                Enrollment.enrollment_date < next_month
            )
            if batch_filter is not None:
                count = query.filter(Enrollment.batch_id.in_(batch_filter)).count() if batch_filter else 0
            else:
                count = query.count()

            months.append(month_start.strftime('%b %Y'))
            counts.append(count)

        return jsonify({
            'success': True,
            'data': {'labels': months, 'data': counts}
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# =============================================
# REVENUE TRENDS  (feeds "Revenue Overview" chart - Admin/Manager only)
# =============================================

@dashboard_bp.route('/revenue-trends', methods=['GET'])
@login_required
@require_module('dashboard')
def get_revenue_trends():
    """Revenue split by payment status. Financial data - Admin/Manager only;
    other roles get zeros since the Revenue Overview card is hidden for them."""
    try:
        if current_user.role not in ('Admin', 'Manager'):
            return jsonify({
                'success': True,
                'data': {'labels': ['Paid', 'Pending', 'Partial'], 'data': [0, 0, 0]}
            })

        paid = Enrollment.query.filter_by(payment_status='Paid').count()
        pending = Enrollment.query.filter_by(payment_status='Pending').count()
        partial = Enrollment.query.filter_by(payment_status='Partial').count()

        return jsonify({
            'success': True,
            'data': {
                'labels': ['Paid', 'Pending', 'Partial'],
                'data': [paid, pending, partial]
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# =============================================
# ATTENDANCE SUMMARY  (feeds "Attendance Overview" chart)
# =============================================

@dashboard_bp.route('/attendance-summary', methods=['GET'])
@login_required
@require_module('dashboard')
def get_attendance_summary():
    """Attendance status breakdown, scoped to the user's role."""
    try:
        query = AttendanceRecord.query

        if current_user.role == 'Instructor':
            if not current_user.instructor_id:
                query = query.filter(db.false())
            else:
                query = query.join(ClassSession).filter(
                    ClassSession.instructor_id == current_user.instructor_id
                )
        elif current_user.role == 'Trainee':
            if not current_user.trainee_id:
                query = query.filter(db.false())
            else:
                query = query.filter(AttendanceRecord.trainee_id == current_user.trainee_id)
        # Admin/Manager: no extra filter - global counts

        present = query.filter(AttendanceRecord.status == 'Present').count()
        absent = query.filter(AttendanceRecord.status == 'Absent').count()
        late = query.filter(AttendanceRecord.status == 'Late').count()
        excused = query.filter(AttendanceRecord.status == 'Excused').count()

        return jsonify({
            'success': True,
            'data': {
                'present': present,
                'absent': absent,
                'late': late,
                'excused': excused
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@dashboard_bp.route('/batch-performance', methods=['GET'])
@login_required
@require_module('dashboard')
def get_batch_performance():
    """Get batch performance data"""
    try:
        upcoming = Batch.query.filter_by(status='Upcoming').count()
        ongoing = Batch.query.filter_by(status='Ongoing').count()
        completed = Batch.query.filter_by(status='Completed').count()
        cancelled = Batch.query.filter_by(status='Cancelled').count()

        return jsonify({
            'success': True,
            'data': {
                'upcoming': upcoming,
                'ongoing': ongoing,
                'completed': completed,
                'cancelled': cancelled
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@dashboard_bp.route('/course-popularity', methods=['GET'])
@login_required
@require_module('dashboard')
def get_course_popularity():
    """Get course popularity data"""
    try:
        courses = Course.query.filter_by(status='Active').limit(5).all()
        data = []
        for course in courses:
            count = Enrollment.query.join(Batch).filter(Batch.course_id == course.course_id).count()
            data.append({
                'course_title': course.course_title,
                'enrollments': count
            })

        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@dashboard_bp.route('/quick-actions', methods=['GET'])
@login_required
@require_module('dashboard')
def get_quick_actions():
    """Get quick actions for dashboard"""
    try:
        return jsonify({
            'success': True,
            'data': [
                {'action': 'Add Trainee', 'icon': 'fa-user-plus', 'link': '/pages/trainees.html'},
                {'action': 'Create Batch', 'icon': 'fa-layer-group', 'link': '/pages/batches.html'},
                {'action': 'New Course', 'icon': 'fa-plus-circle', 'link': '/pages/courses.html'},
                {'action': 'Generate Certificate', 'icon': 'fa-certificate', 'link': '/pages/certificates.html'}
            ]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@dashboard_bp.route('/full', methods=['GET'])
@login_required
@require_module('dashboard')
def get_full_dashboard():
    """Get full dashboard data"""
    try:
        stats = get_stats().json['data']
        attendance = get_attendance_summary().json['data']

        data = {'stats': stats, 'attendance': attendance}
        if current_user.role in ('Admin', 'Manager'):
            data['overview'] = get_overview().json['data']

        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# =============================================
# RECENT ACTIVITY  (feeds "Recent Activity" panel)
# =============================================

@dashboard_bp.route('/activities', methods=['GET'])
@login_required
@require_module('dashboard')
def get_activities():
    """Recent activity, scoped to the user's role."""
    try:
        activities = []

        if current_user.role in ('Admin', 'Manager'):
            recent_enrollments = Enrollment.query.order_by(
                Enrollment.enrollment_date.desc()
            ).limit(5).all()

            recent_certs = Certificate.query.filter(
                Certificate.status == 'Issued'
            ).order_by(Certificate.issue_date.desc()).limit(5).all()

        elif current_user.role == 'Instructor':
            batch_ids = _instructor_batch_ids()
            if batch_ids:
                recent_enrollments = Enrollment.query.filter(
                    Enrollment.batch_id.in_(batch_ids)
                ).order_by(Enrollment.enrollment_date.desc()).limit(5).all()

                recent_certs = Certificate.query.join(Enrollment).filter(
                    Enrollment.batch_id.in_(batch_ids),
                    Certificate.status == 'Issued'
                ).order_by(Certificate.issue_date.desc()).limit(5).all()
            else:
                recent_enrollments = []
                recent_certs = []

        elif current_user.role == 'Trainee':
            if current_user.trainee_id:
                recent_enrollments = Enrollment.query.filter_by(
                    trainee_id=current_user.trainee_id
                ).order_by(Enrollment.enrollment_date.desc()).limit(5).all()

                recent_certs = Certificate.query.join(Enrollment).filter(
                    Enrollment.trainee_id == current_user.trainee_id,
                    Certificate.status == 'Issued'
                ).order_by(Certificate.issue_date.desc()).limit(5).all()
            else:
                recent_enrollments = []
                recent_certs = []
        else:
            recent_enrollments = []
            recent_certs = []

        for enrollment in recent_enrollments:
            trainee = enrollment.trainee
            batch = enrollment.batch
            if trainee and batch:
                activities.append({
                    'message': f'New enrollment: {trainee.first_name} {trainee.last_name} enrolled in {batch.batch_name}',
                    'time_ago': 'Just now',
                    'icon': 'fa-user-plus',
                    'iconBg': 'bg-success-light'
                })

        for cert in recent_certs:
            enrollment = cert.enrollment
            if enrollment and enrollment.trainee:
                activities.append({
                    'message': f'Certificate issued: {enrollment.trainee.first_name} {enrollment.trainee.last_name}',
                    'time_ago': 'Just now',
                    'icon': 'fa-certificate',
                    'iconBg': 'bg-warning-light'
                })

        return jsonify({
            'success': True,
            'data': activities
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
