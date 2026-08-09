from flask import Blueprint
from flask_login import login_required
from controllers.report_controller import ReportController
from utils.decorators import require_module

report_bp = Blueprint('report', __name__, url_prefix='/api/reports')

@report_bp.route('/active-trainees', methods=['GET'])
@login_required
@require_module('reports')
def get_active_trainees_report():
    """Generate active trainees report"""
    return ReportController.get_active_trainees_report()

@report_bp.route('/instructor-workload', methods=['GET'])
@login_required
@require_module('reports')
def get_instructor_workload_report():
    """Generate instructor workload report"""
    return ReportController.get_instructor_workload_report()

@report_bp.route('/course-enrollment', methods=['GET'])
@login_required
@require_module('reports')
def get_course_enrollment_report():
    """Generate course enrollment statistics report"""
    return ReportController.get_course_enrollment_report()

@report_bp.route('/batch-capacity', methods=['GET'])
@login_required
@require_module('reports')
def get_batch_capacity_report():
    """Generate batch capacity report"""
    return ReportController.get_batch_capacity_report()

@report_bp.route('/payment-status', methods=['GET'])
@login_required
@require_module('reports')
def get_payment_status_report():
    """Generate payment status report"""
    return ReportController.get_payment_status_report()

@report_bp.route('/attendance', methods=['GET'])
@login_required
@require_module('reports')
def get_attendance_report():
    """Generate attendance report"""
    return ReportController.get_attendance_report()

@report_bp.route('/assessment-results', methods=['GET'])
@login_required
@require_module('reports')
def get_assessment_results_report():
    """Generate assessment results report"""
    return ReportController.get_assessment_results_report()

@report_bp.route('/certificates', methods=['GET'])
@login_required
@require_module('reports')
def get_certificate_report():
    """Generate certificate issuance report"""
    return ReportController.get_certificate_report()
