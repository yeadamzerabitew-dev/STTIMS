from flask import request, jsonify
from flask_login import login_required, current_user
from models import (
    Trainee, Instructor, Course, Batch, Enrollment,
    AttendanceRecord, Certificate, ClassSession, Assessment,
    TraineeResult, db
)
from utils.decorators import role_required
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_, extract

class DashboardController:
    """Controller for dashboard statistics"""
    
    # =============================================
    # OVERVIEW STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    def get_overview():
        """Get overview dashboard statistics"""
        try:
            # Get counts
            total_trainees = Trainee.query.filter_by(status='Active').count()
            total_instructors = Instructor.query.filter_by(status='Active').count()
            total_courses = Course.query.filter_by(status='Active').count()
            
            # Batch counts
            upcoming_batches = Batch.query.filter_by(status='Upcoming').count()
            ongoing_batches = Batch.query.filter_by(status='Ongoing').count()
            completed_batches = Batch.query.filter_by(status='Completed').count()
            cancelled_batches = Batch.query.filter_by(status='Cancelled').count()
            
            # Enrollment counts
            active_enrollments = Enrollment.query.filter_by(status='Active').count()
            total_enrollments = Enrollment.query.count()
            completed_enrollments = Enrollment.query.filter_by(status='Completed').count()
            dropped_enrollments = Enrollment.query.filter_by(status='Dropped').count()
            
            # Attendance
            attendance_records = AttendanceRecord.query.filter(
                AttendanceRecord.status.in_(['Present', 'Late'])
            ).count()
            total_attendance = AttendanceRecord.query.count()
            attendance_rate = round(
                (attendance_records / total_attendance) * 100, 2
            ) if total_attendance > 0 else 0
            
            # Certificates
            certificates_issued = Certificate.query.filter_by(status='Issued').count()
            total_certificates = Certificate.query.count()
            
            # Revenue
            total_revenue = db.session.query(
                func.sum(Enrollment.payment_amount)
            ).filter(Enrollment.payment_status == 'Paid').scalar() or 0
            
            pending_revenue = db.session.query(
                func.sum(Enrollment.final_amount)
            ).filter(Enrollment.payment_status == 'Pending').scalar() or 0
            
            # Recent activity (last 7 days)
            seven_days_ago = date.today() - timedelta(days=7)
            recent_enrollments = Enrollment.query.filter(
                Enrollment.created_at >= seven_days_ago
            ).count()
            
            recent_certificates = Certificate.query.filter(
                Certificate.created_at >= seven_days_ago
            ).count()
            
            return jsonify({
                'overview': {
                    'total_trainees': total_trainees,
                    'total_instructors': total_instructors,
                    'total_courses': total_courses,
                    'upcoming_batches': upcoming_batches,
                    'ongoing_batches': ongoing_batches,
                    'completed_batches': completed_batches,
                    'cancelled_batches': cancelled_batches,
                    'active_enrollments': active_enrollments,
                    'total_enrollments': total_enrollments,
                    'completed_enrollments': completed_enrollments,
                    'dropped_enrollments': dropped_enrollments,
                    'attendance_rate': attendance_rate,
                    'certificates_issued': certificates_issued,
                    'total_certificates': total_certificates,
                    'total_revenue': float(total_revenue),
                    'pending_revenue': float(pending_revenue)
                },
                'recent_activity': {
                    'recent_enrollments': recent_enrollments,
                    'recent_certificates': recent_certificates,
                    'days': 7
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # ENROLLMENT TRENDS
    # =============================================
    
    @staticmethod
    @login_required
    def get_enrollment_trends():
        """Get enrollment trends over time"""
        try:
            # Get last 6 months
            months = []
            enrollments = []
            completed = []
            
            for i in range(5, -1, -1):
                month_date = date.today().replace(day=1) - timedelta(days=i*30)
                month_key = month_date.strftime('%Y-%m')
                months.append(month_date.strftime('%b %Y'))
                
                # Count enrollments for this month
                count = Enrollment.query.filter(
                    func.date_format(Enrollment.enrollment_date, '%Y-%m') == month_key
                ).count()
                enrollments.append(count)
                
                # Count completed for this month
                completed_count = Enrollment.query.filter(
                    func.date_format(Enrollment.completion_date, '%Y-%m') == month_key,
                    Enrollment.status == 'Completed'
                ).count()
                completed.append(completed_count)
            
            return jsonify({
                'labels': months,
                'enrollments': enrollments,
                'completed': completed
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # REVENUE TRENDS
    # =============================================
    
    @staticmethod
    @login_required
    def get_revenue_trends():
        """Get revenue trends over time"""
        try:
            # Get last 6 months
            months = []
            revenue = []
            expected = []
            
            for i in range(5, -1, -1):
                month_date = date.today().replace(day=1) - timedelta(days=i*30)
                month_key = month_date.strftime('%Y-%m')
                months.append(month_date.strftime('%b %Y'))
                
                # Sum revenue for this month
                rev = db.session.query(
                    func.sum(Enrollment.payment_amount)
                ).filter(
                    func.date_format(Enrollment.payment_date, '%Y-%m') == month_key,
                    Enrollment.payment_status == 'Paid'
                ).scalar() or 0
                revenue.append(float(rev))
                
                # Sum expected revenue for this month
                exp = db.session.query(
                    func.sum(Enrollment.final_amount)
                ).filter(
                    func.date_format(Enrollment.enrollment_date, '%Y-%m') == month_key
                ).scalar() or 0
                expected.append(float(exp))
            
            return jsonify({
                'labels': months,
                'revenue': revenue,
                'expected': expected
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # BATCH PERFORMANCE
    # =============================================
    
    @staticmethod
    @login_required
    def get_batch_performance():
        """Get batch performance metrics"""
        try:
            # Get ongoing batches
            batches = Batch.query.filter_by(status='Ongoing').all()
            
            batch_data = []
            for batch in batches:
                total_enrolled = batch.enrollments.filter_by(status='Active').count()
                capacity_utilization = round(
                    (total_enrolled / batch.max_capacity) * 100, 2
                ) if batch.max_capacity > 0 else 0
                
                # Average attendance for this batch
                avg_attendance = db.session.query(
                    func.avg(Enrollment.attendance_percentage)
                ).filter(
                    Enrollment.batch_id == batch.batch_id,
                    Enrollment.status == 'Active'
                ).scalar() or 0
                
                # Average completion
                avg_completion = db.session.query(
                    func.avg(Enrollment.completion_percentage)
                ).filter(
                    Enrollment.batch_id == batch.batch_id,
                    Enrollment.status == 'Active'
                ).scalar() or 0
                
                batch_data.append({
                    'batch_id': batch.batch_id,
                    'batch_name': batch.batch_name,
                    'course_title': batch.course.course_title,
                    'total_enrolled': total_enrolled,
                    'max_capacity': batch.max_capacity,
                    'capacity_utilization': capacity_utilization,
                    'avg_attendance': round(avg_attendance, 2),
                    'avg_completion': round(avg_completion, 2),
                    'start_date': batch.start_date.isoformat(),
                    'end_date': batch.end_date.isoformat(),
                    'days_remaining': (batch.end_date - date.today()).days
                })
            
            return jsonify({
                'ongoing_batches': batch_data,
                'total_ongoing': len(batch_data)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # ATTENDANCE SUMMARY
    # =============================================
    
    @staticmethod
    @login_required
    def get_attendance_summary():
        """Get attendance summary"""
        try:
            # Overall attendance
            present = AttendanceRecord.query.filter_by(status='Present').count()
            absent = AttendanceRecord.query.filter_by(status='Absent').count()
            late = AttendanceRecord.query.filter_by(status='Late').count()
            excused = AttendanceRecord.query.filter_by(status='Excused').count()
            
            total = present + absent + late + excused
            
            # Attendance by session type
            session_attendance = db.session.query(
                ClassSession.session_type,
                func.count(AttendanceRecord.attendance_id).label('total'),
                func.sum(case((AttendanceRecord.status == 'Present', 1), else_=0)).label('present')
            ).join(
                AttendanceRecord, ClassSession.session_id == AttendanceRecord.session_id
            ).group_by(
                ClassSession.session_type
            ).all()
            
            session_data = []
            for item in session_attendance:
                session_data.append({
                    'session_type': item.session_type,
                    'total': item.total,
                    'present': item.present,
                    'rate': round((item.present / item.total) * 100, 2) if item.total > 0 else 0
                })
            
            return jsonify({
                'attendance': {
                    'present': present,
                    'absent': absent,
                    'late': late,
                    'excused': excused,
                    'total': total,
                    'rate': round((present / total) * 100, 2) if total > 0 else 0
                },
                'by_session_type': session_data
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # COURSE POPULARITY
    # =============================================
    
    @staticmethod
    @login_required
    def get_course_popularity():
        """Get course popularity rankings"""
        try:
            # Get top courses by enrollment
            course_data = db.session.query(
                Course.course_id,
                Course.course_title,
                func.count(Enrollment.enrollment_id).label('enrollments'),
                func.sum(Enrollment.payment_amount).label('revenue')
            ).join(
                Batch, Batch.course_id == Course.course_id
            ).join(
                Enrollment, Enrollment.batch_id == Batch.batch_id
            ).filter(
                Enrollment.status != 'Dropped'
            ).group_by(
                Course.course_id
            ).order_by(
                func.count(Enrollment.enrollment_id).desc()
            ).limit(10).all()
            
            courses = []
            for item in course_data:
                courses.append({
                    'course_id': item.course_id,
                    'course_title': item.course_title,
                    'enrollments': item.enrollments,
                    'revenue': float(item.revenue) if item.revenue else 0
                })
            
            return jsonify({
                'top_courses': courses
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # QUICK ACTIONS
    # =============================================
    
    @staticmethod
    @login_required
    def get_quick_actions():
        """Get quick action items for dashboard"""
        try:
            # Check for pending tasks
            pending_actions = []
            
            # Check low attendance trainees
            low_attendance = Enrollment.query.filter(
                Enrollment.attendance_percentage < 75,
                Enrollment.status == 'Active'
            ).count()
            if low_attendance > 0:
                pending_actions.append({
                    'type': 'warning',
                    'title': f'{low_attendance} trainees have low attendance',
                    'link': '/reports/attendance'
                })
            
            # Check batches with low enrollment
            low_enrollment = Batch.query.filter(
                Batch.current_enrollment < Batch.min_trainees_required,
                Batch.status == 'Upcoming'
            ).count()
            if low_enrollment > 0:
                pending_actions.append({
                    'type': 'danger',
                    'title': f'{low_enrollment} batches have low enrollment',
                    'link': '/batches'
                })
            
            # Check pending certificates
            pending_certificates = Certificate.query.filter(
                Certificate.status == 'Pending'
            ).count()
            if pending_certificates > 0:
                pending_actions.append({
                    'type': 'info',
                    'title': f'{pending_certificates} certificates pending approval',
                    'link': '/certificates'
                })
            
            # Check upcoming batches
            upcoming = Batch.query.filter(
                Batch.status == 'Upcoming',
                Batch.start_date <= date.today() + timedelta(days=7)
            ).count()
            if upcoming > 0:
                pending_actions.append({
                    'type': 'success',
                    'title': f'{upcoming} batches starting in the next 7 days',
                    'link': '/batches'
                })
            
            return jsonify({
                'pending_actions': pending_actions,
                'total_actions': len(pending_actions)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # COMPLETE DASHBOARD
    # =============================================
    
    @staticmethod
    @login_required
    def get_full_dashboard():
        """Get complete dashboard data"""
        try:
            overview = DashboardController.get_overview()
            if overview[1] != 200:
                return overview
            
            enrollment_trends = DashboardController.get_enrollment_trends()
            revenue_trends = DashboardController.get_revenue_trends()
            batch_performance = DashboardController.get_batch_performance()
            attendance_summary = DashboardController.get_attendance_summary()
            course_popularity = DashboardController.get_course_popularity()
            quick_actions = DashboardController.get_quick_actions()
            
            return jsonify({
                'overview': overview[0].json['overview'],
                'recent_activity': overview[0].json['recent_activity'],
                'enrollment_trends': enrollment_trends[0].json,
                'revenue_trends': revenue_trends[0].json,
                'batch_performance': batch_performance[0].json,
                'attendance_summary': attendance_summary[0].json,
                'course_popularity': course_popularity[0].json,
                'quick_actions': quick_actions[0].json
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
