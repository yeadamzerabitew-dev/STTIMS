from flask import request, jsonify, Response
from flask_login import login_required, current_user
from models import (
    Trainee, Instructor, Course, Batch, Enrollment,
    AttendanceRecord, Assessment, TraineeResult,
    Certificate, Category, db
)
from utils.decorators import role_required
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_, extract
import csv
import io
import json

class ReportController:
    """Controller for report generation"""
    
    # =============================================
    # 1. ACTIVE TRAINEES REPORT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_active_trainees_report():
        """Generate active trainees report"""
        try:
            # Get query parameters
            search = request.args.get('search', '')
            gender = request.args.get('gender', '')
            educational_level = request.args.get('educational_level', '')
            sort_by = request.args.get('sort_by', 'trainee_id')
            sort_order = request.args.get('sort_order', 'desc')
            format = request.args.get('format', 'json')  # json or csv
            
            query = Trainee.query.filter_by(status='Active')
            
            if search:
                query = query.filter(
                    (Trainee.first_name.ilike(f'%{search}%')) |
                    (Trainee.last_name.ilike(f'%{search}%')) |
                    (Trainee.email.ilike(f'%{search}%')) |
                    (Trainee.trainee_code.ilike(f'%{search}%'))
                )
            
            if gender:
                query = query.filter(Trainee.gender == gender)
            
            if educational_level:
                query = query.filter(Trainee.educational_level == educational_level)
            
            # Apply sorting
            valid_sort_fields = ['trainee_id', 'trainee_code', 'first_name', 'last_name', 
                                 'email', 'registration_date', 'educational_level']
            if sort_by in valid_sort_fields:
                if sort_order.lower() == 'asc':
                    query = query.order_by(getattr(Trainee, sort_by).asc())
                else:
                    query = query.order_by(getattr(Trainee, sort_by).desc())
            
            trainees = query.all()
            
            # Prepare report data
            report_data = []
            for trainee in trainees:
                enrollments = trainee.enrollments.all()
                total_enrollments = len(enrollments)
                active_enrollments = sum(1 for e in enrollments if e.status == 'Active')
                completed_enrollments = sum(1 for e in enrollments if e.status == 'Completed')
                
                report_data.append({
                    'trainee_id': trainee.trainee_id,
                    'trainee_code': trainee.trainee_code,
                    'full_name': trainee.full_name,
                    'email': trainee.email,
                    'phone': trainee.phone_number,
                    'gender': trainee.gender,
                    'educational_level': trainee.educational_level,
                    'occupation': trainee.occupation,
                    'organization': trainee.organization,
                    'registration_date': trainee.registration_date.isoformat() if trainee.registration_date else None,
                    'age': trainee.age,
                    'total_enrollments': total_enrollments,
                    'active_enrollments': active_enrollments,
                    'completed_enrollments': completed_enrollments,
                    'overall_attendance': trainee.overall_attendance,
                    'overall_completion': trainee.overall_completion
                })
            
            # Summary statistics
            total = len(report_data)
            male_count = sum(1 for t in report_data if t['gender'] == 'Male')
            female_count = sum(1 for t in report_data if t['gender'] == 'Female')
            avg_age = sum(t['age'] or 0 for t in report_data) / total if total > 0 else 0
            
            summary = {
                'total_trainees': total,
                'male': male_count,
                'female': female_count,
                'avg_age': round(avg_age, 1),
                'educational_levels': {}
            }
            
            for trainee in report_data:
                level = trainee['educational_level']
                summary['educational_levels'][level] = summary['educational_levels'].get(level, 0) + 1
            
            if format == 'csv':
                return ReportController._export_csv(report_data, 'active_trainees_report')
            
            return jsonify({
                'report_name': 'Active Trainees Report',
                'generated_at': datetime.now().isoformat(),
                'summary': summary,
                'data': report_data,
                'total_records': len(report_data)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # 2. INSTRUCTOR WORKLOAD REPORT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_instructor_workload_report():
        """Generate instructor workload report"""
        try:
            status = request.args.get('status', 'Active')
            format = request.args.get('format', 'json')
            
            query = Instructor.query
            
            if status:
                query = query.filter(Instructor.status == status)
            
            instructors = query.all()
            
            report_data = []
            total_workload = 0
            
            for instructor in instructors:
                assignments = instructor.course_assignments.filter_by(status='Active').all()
                total_batches = len(assignments)
                total_hours = sum(a.teaching_hours or 0 for a in assignments)
                total_trainees = 0
                
                for assignment in assignments:
                    batch = assignment.batch
                    if batch:
                        total_trainees += batch.enrollments.filter_by(status='Active').count()
                
                # Get specializations
                specializations = [s.skill_name for s in instructor.specializations.all()]
                
                report_data.append({
                    'instructor_id': instructor.instructor_id,
                    'instructor_code': instructor.instructor_code,
                    'full_name': instructor.full_name,
                    'email': instructor.email,
                    'phone': instructor.phone_number,
                    'department': instructor.department,
                    'qualification': instructor.qualification,
                    'years_of_experience': instructor.years_of_experience,
                    'employment_type': instructor.employment_type,
                    'status': instructor.status,
                    'total_batches': total_batches,
                    'total_teaching_hours': total_hours,
                    'total_trainees': total_trainees,
                    'specializations': specializations,
                    'workload_score': round((total_batches * 10) + (total_hours * 0.5), 2)
                })
                
                total_workload += total_hours
            
            # Summary
            summary = {
                'total_instructors': len(report_data),
                'total_teaching_hours': total_workload,
                'avg_hours_per_instructor': round(total_workload / len(report_data), 2) if report_data else 0,
                'avg_batches_per_instructor': round(sum(d['total_batches'] for d in report_data) / len(report_data), 2) if report_data else 0
            }
            
            if format == 'csv':
                return ReportController._export_csv(report_data, 'instructor_workload_report')
            
            return jsonify({
                'report_name': 'Instructor Workload Report',
                'generated_at': datetime.now().isoformat(),
                'summary': summary,
                'data': report_data,
                'total_records': len(report_data)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # 3. COURSE ENROLLMENT STATISTICS
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_course_enrollment_report():
        """Generate course enrollment statistics report"""
        try:
            category_id = request.args.get('category_id', type=int)
            status = request.args.get('status', 'Active')
            format = request.args.get('format', 'json')
            
            query = Course.query
            
            if category_id:
                query = query.filter(Course.category_id == category_id)
            if status:
                query = query.filter(Course.status == status)
            
            courses = query.all()
            
            report_data = []
            total_enrollments = 0
            total_revenue = 0
            
            for course in courses:
                batches = course.batches.all()
                total_batches = len(batches)
                total_capacity = sum(b.max_capacity for b in batches)
                total_enrolled = 0
                total_completed = 0
                revenue = 0
                
                for batch in batches:
                    enrollments = batch.enrollments.all()
                    total_enrolled += len(enrollments)
                    total_completed += sum(1 for e in enrollments if e.status == 'Completed')
                    revenue += sum(e.payment_amount or 0 for e in enrollments if e.payment_status == 'Paid')
                
                utilization = round((total_enrolled / total_capacity) * 100, 2) if total_capacity > 0 else 0
                completion_rate = round((total_completed / total_enrolled) * 100, 2) if total_enrolled > 0 else 0
                
                report_data.append({
                    'course_id': course.course_id,
                    'course_code': course.course_code,
                    'course_title': course.course_title,
                    'category': course.category.category_name if course.category else None,
                    'level': course.course_level,
                    'fee': float(course.fee_amount),
                    'total_batches': total_batches,
                    'total_capacity': total_capacity,
                    'total_enrolled': total_enrolled,
                    'total_completed': total_completed,
                    'utilization_rate': utilization,
                    'completion_rate': completion_rate,
                    'revenue': float(revenue),
                    'avg_per_batch': round(total_enrolled / total_batches, 2) if total_batches > 0 else 0
                })
                
                total_enrollments += total_enrolled
                total_revenue += revenue
            
            # Summary
            summary = {
                'total_courses': len(report_data),
                'total_enrollments': total_enrollments,
                'total_revenue': float(total_revenue),
                'avg_enrollment_per_course': round(total_enrollments / len(report_data), 2) if report_data else 0,
                'avg_completion_rate': round(sum(d['completion_rate'] for d in report_data) / len(report_data), 2) if report_data else 0
            }
            
            if format == 'csv':
                return ReportController._export_csv(report_data, 'course_enrollment_report')
            
            return jsonify({
                'report_name': 'Course Enrollment Statistics',
                'generated_at': datetime.now().isoformat(),
                'summary': summary,
                'data': report_data,
                'total_records': len(report_data)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # 4. BATCH CAPACITY REPORT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_batch_capacity_report():
        """Generate batch capacity report"""
        try:
            status = request.args.get('status', '')
            format = request.args.get('format', 'json')
            
            query = Batch.query
            
            if status:
                query = query.filter(Batch.status == status)
            
            batches = query.all()
            
            report_data = []
            total_capacity = 0
            total_enrolled = 0
            total_available = 0
            
            for batch in batches:
                available = batch.max_capacity - batch.current_enrollment
                occupancy = round((batch.current_enrollment / batch.max_capacity) * 100, 2) if batch.max_capacity > 0 else 0
                
                report_data.append({
                    'batch_id': batch.batch_id,
                    'batch_code': batch.batch_code,
                    'batch_name': batch.batch_name,
                    'course_title': batch.course.course_title,
                    'start_date': batch.start_date.isoformat(),
                    'end_date': batch.end_date.isoformat(),
                    'schedule_type': batch.schedule_type,
                    'max_capacity': batch.max_capacity,
                    'current_enrollment': batch.current_enrollment,
                    'available_slots': available,
                    'occupancy_rate': occupancy,
                    'status': batch.status,
                    'min_trainees_required': batch.min_trainees_required,
                    'instructor': batch.instructor.full_name if batch.instructor else None
                })
                
                total_capacity += batch.max_capacity
                total_enrolled += batch.current_enrollment
                total_available += available
            
            # Summary
            summary = {
                'total_batches': len(report_data),
                'total_capacity': total_capacity,
                'total_enrolled': total_enrolled,
                'total_available': total_available,
                'overall_occupancy': round((total_enrolled / total_capacity) * 100, 2) if total_capacity > 0 else 0,
                'full_batches': sum(1 for d in report_data if d['occupancy_rate'] >= 90),
                'empty_batches': sum(1 for d in report_data if d['occupancy_rate'] == 0),
                'under_enrolled': sum(1 for d in report_data if d['current_enrollment'] < d.get('min_trainees_required', 5))
            }
            
            if format == 'csv':
                return ReportController._export_csv(report_data, 'batch_capacity_report')
            
            return jsonify({
                'report_name': 'Batch Capacity Report',
                'generated_at': datetime.now().isoformat(),
                'summary': summary,
                'data': report_data,
                'total_records': len(report_data)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # 5. PAYMENT STATUS REPORT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_payment_status_report():
        """Generate payment status report"""
        try:
            payment_status = request.args.get('payment_status', '')
            date_from = request.args.get('date_from')
            date_to = request.args.get('date_to')
            format = request.args.get('format', 'json')
            
            query = Enrollment.query
            
            if payment_status:
                query = query.filter(Enrollment.payment_status == payment_status)
            
            if date_from:
                query = query.filter(Enrollment.enrollment_date >= date_from)
            if date_to:
                query = query.filter(Enrollment.enrollment_date <= date_to)
            
            enrollments = query.all()
            
            report_data = []
            total_paid = 0
            total_pending = 0
            total_expected = 0
            
            for enrollment in enrollments:
                report_data.append({
                    'enrollment_id': enrollment.enrollment_id,
                    'enrollment_number': enrollment.enrollment_number,
                    'trainee_name': enrollment.trainee.full_name if enrollment.trainee else None,
                    'course_title': enrollment.batch.course.course_title if enrollment.batch else None,
                    'batch_name': enrollment.batch.batch_name if enrollment.batch else None,
                    'enrollment_date': enrollment.enrollment_date.isoformat(),
                    'payment_status': enrollment.payment_status,
                    'payment_amount': float(enrollment.payment_amount) if enrollment.payment_amount else 0,
                    'discount_amount': float(enrollment.discount_amount),
                    'final_amount': float(enrollment.final_amount) if enrollment.final_amount else 0,
                    'payment_method': enrollment.payment_method,
                    'payment_date': enrollment.payment_date.isoformat() if enrollment.payment_date else None,
                    'status': enrollment.status
                })
                
                total_paid += enrollment.payment_amount or 0
                total_pending += enrollment.final_amount or 0
                total_expected += enrollment.final_amount or 0
            
            # Summary by payment status
            status_summary = {}
            for status in ['Paid', 'Pending', 'Partial', 'Scholarship']:
                count = sum(1 for d in report_data if d['payment_status'] == status)
                amount = sum(d['payment_amount'] for d in report_data if d['payment_status'] == status)
                status_summary[status] = {'count': count, 'amount': float(amount)}
            
            summary = {
                'total_enrollments': len(report_data),
                'total_paid': float(total_paid),
                'total_pending': float(total_pending - total_paid),
                'total_expected': float(total_expected),
                'collection_rate': round((total_paid / total_expected) * 100, 2) if total_expected > 0 else 0,
                'by_status': status_summary
            }
            
            if format == 'csv':
                return ReportController._export_csv(report_data, 'payment_status_report')
            
            return jsonify({
                'report_name': 'Payment Status Report',
                'generated_at': datetime.now().isoformat(),
                'summary': summary,
                'data': report_data,
                'total_records': len(report_data)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # 6. ATTENDANCE REPORT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def get_attendance_report():
        """Generate attendance report"""
        try:
            batch_id = request.args.get('batch_id', type=int)
            trainee_id = request.args.get('trainee_id', type=int)
            date_from = request.args.get('date_from')
            date_to = request.args.get('date_to')
            format = request.args.get('format', 'json')
            
            query = AttendanceRecord.query
            
            if batch_id:
                query = query.join(ClassSession).filter(ClassSession.batch_id == batch_id)
            
            if trainee_id:
                query = query.filter(AttendanceRecord.trainee_id == trainee_id)
            
            if date_from:
                query = query.join(ClassSession).filter(ClassSession.session_date >= date_from)
            if date_to:
                query = query.join(ClassSession).filter(ClassSession.session_date <= date_to)
            
            records = query.all()
            
            report_data = []
            present_count = 0
            absent_count = 0
            late_count = 0
            excused_count = 0
            
            for record in records:
                report_data.append({
                    'record_id': record.attendance_id,
                    'trainee_name': record.trainee.full_name if record.trainee else None,
                    'trainee_code': record.trainee.trainee_code if record.trainee else None,
                    'session_date': record.session.session_date.isoformat() if record.session else None,
                    'topic': record.session.topic_covered if record.session else None,
                    'session_type': record.session.session_type if record.session else None,
                    'batch_name': record.session.batch.batch_name if record.session and record.session.batch else None,
                    'status': record.status,
                    'check_in_time': record.check_in_time.strftime('%H:%M') if record.check_in_time else None,
                    'check_out_time': record.check_out_time.strftime('%H:%M') if record.check_out_time else None,
                    'remarks': record.remarks,
                    'recorded_by': record.recorded_by,
                    'recorded_at': record.recorded_at.isoformat() if record.recorded_at else None,
                    'is_verified': record.is_verified
                })
                
                if record.status == 'Present':
                    present_count += 1
                elif record.status == 'Absent':
                    absent_count += 1
                elif record.status == 'Late':
                    late_count += 1
                elif record.status == 'Excused':
                    excused_count += 1
            
            total = len(report_data)
            
            summary = {
                'total_records': total,
                'present': present_count,
                'absent': absent_count,
                'late': late_count,
                'excused': excused_count,
                'attendance_rate': round((present_count / total) * 100, 2) if total > 0 else 0
            }
            
            if format == 'csv':
                return ReportController._export_csv(report_data, 'attendance_report')
            
            return jsonify({
                'report_name': 'Attendance Report',
                'generated_at': datetime.now().isoformat(),
                'summary': summary,
                'data': report_data,
                'total_records': len(report_data)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # 7. ASSESSMENT RESULTS REPORT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager', 'Instructor'])
    def get_assessment_results_report():
        """Generate assessment results report"""
        try:
            assessment_id = request.args.get('assessment_id', type=int)
            batch_id = request.args.get('batch_id', type=int)
            format = request.args.get('format', 'json')
            
            query = TraineeResult.query
            
            if assessment_id:
                query = query.filter(TraineeResult.assessment_id == assessment_id)
            elif batch_id:
                query = query.join(Assessment).filter(Assessment.batch_id == batch_id)
            
            results = query.all()
            
            report_data = []
            passed_count = 0
            failed_count = 0
            not_attempted = 0
            total_marks = 0
            
            for result in results:
                report_data.append({
                    'result_id': result.result_id,
                    'trainee_name': result.trainee.full_name if result.trainee else None,
                    'trainee_code': result.trainee.trainee_code if result.trainee else None,
                    'assessment_title': result.assessment.title if result.assessment else None,
                    'assessment_type': result.assessment.assessment_type if result.assessment else None,
                    'max_marks': result.assessment.max_marks if result.assessment else 0,
                    'marks_obtained': float(result.marks_obtained) if result.marks_obtained is not None else None,
                    'percentage_score': float(result.percentage_score) if result.percentage_score is not None else None,
                    'grade': result.grade,
                    'status': result.status,
                    'comments': result.comments,
                    'instructor_feedback': result.instructor_feedback,
                    'recorded_at': result.recorded_at.isoformat() if result.recorded_at else None,
                    'is_verified': result.is_verified
                })
                
                if result.status == 'Pass':
                    passed_count += 1
                elif result.status == 'Fail':
                    failed_count += 1
                else:
                    not_attempted += 1
                
                if result.marks_obtained is not None:
                    total_marks += result.marks_obtained
            
            total = len(report_data)
            
            summary = {
                'total_results': total,
                'passed': passed_count,
                'failed': failed_count,
                'not_attempted': not_attempted,
                'pass_rate': round((passed_count / (passed_count + failed_count)) * 100, 2) if (passed_count + failed_count) > 0 else 0,
                'average_marks': round(total_marks / total, 2) if total > 0 else 0
            }
            
            if format == 'csv':
                return ReportController._export_csv(report_data, 'assessment_results_report')
            
            return jsonify({
                'report_name': 'Assessment Results Report',
                'generated_at': datetime.now().isoformat(),
                'summary': summary,
                'data': report_data,
                'total_records': len(report_data)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # 8. CERTIFICATE ISSUANCE REPORT
    # =============================================
    
    @staticmethod
    @login_required
    @role_required(['Admin', 'Manager'])
    def get_certificate_report():
        """Generate certificate issuance report"""
        try:
            status = request.args.get('status', '')
            date_from = request.args.get('date_from')
            date_to = request.args.get('date_to')
            format = request.args.get('format', 'json')
            
            query = Certificate.query
            
            if status:
                query = query.filter(Certificate.status == status)
            if date_from:
                query = query.filter(Certificate.issue_date >= date_from)
            if date_to:
                query = query.filter(Certificate.issue_date <= date_to)
            
            certificates = query.all()
            
            report_data = []
            issued_count = 0
            revoked_count = 0
            expired_count = 0
            pending_count = 0
            
            for cert in certificates:
                report_data.append({
                    'certificate_id': cert.certificate_id,
                    'certificate_number': cert.certificate_number,
                    'trainee_name': cert.enrollment.trainee.full_name if cert.enrollment else None,
                    'trainee_code': cert.enrollment.trainee.trainee_code if cert.enrollment else None,
                    'course_title': cert.enrollment.batch.course.course_title if cert.enrollment else None,
                    'batch_name': cert.enrollment.batch.batch_name if cert.enrollment else None,
                    'grade': cert.enrollment.grade if cert.enrollment else None,
                    'issue_date': cert.issue_date.isoformat(),
                    'expiry_date': cert.expiry_date.isoformat() if cert.expiry_date else None,
                    'status': cert.status,
                    'verification_token': cert.verification_token,
                    'approved_by': cert.approved_by,
                    'notes': cert.notes,
                    'created_at': cert.created_at.isoformat() if cert.created_at else None
                })
                
                if cert.status == 'Issued':
                    issued_count += 1
                elif cert.status == 'Revoked':
                    revoked_count += 1
                elif cert.status == 'Expired':
                    expired_count += 1
                elif cert.status == 'Pending':
                    pending_count += 1
            
            total = len(report_data)
            
            summary = {
                'total_certificates': total,
                'issued': issued_count,
                'revoked': revoked_count,
                'expired': expired_count,
                'pending': pending_count,
                'active_certificates': issued_count - expired_count
            }
            
            if format == 'csv':
                return ReportController._export_csv(report_data, 'certificate_report')
            
            return jsonify({
                'report_name': 'Certificate Issuance Report',
                'generated_at': datetime.now().isoformat(),
                'summary': summary,
                'data': report_data,
                'total_records': len(report_data)
            }), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================
    # CSV EXPORT HELPER
    # =============================================
    
    @staticmethod
    def _export_csv(data, filename):
        """Export data as CSV"""
        try:
            if not data:
                return jsonify({'error': 'No data to export'}), 400
            
            # Create CSV
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write headers
            headers = list(data[0].keys())
            writer.writerow(headers)
            
            # Write data
            for row in data:
                writer.writerow([row.get(h, '') for h in headers])
            
            # Create response
            response = Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename={filename}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                }
            )
            return response
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
