from flask import Blueprint
from flask_login import login_required
from controllers.attendance_controller import AttendanceController
from utils.decorators import require_module

attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')

@attendance_bp.route('/', methods=['GET'])
@login_required
@require_module('attendance')
def list_attendance():
    """List all attendance records with filters and pagination"""
    return AttendanceController.list_attendance()

@attendance_bp.route('/', methods=['POST'])
@login_required
@require_module('attendance')
def mark_attendance():
    """Mark attendance for a single trainee"""
    return AttendanceController.mark_attendance()

@attendance_bp.route('/bulk', methods=['POST'])
@login_required
@require_module('attendance')
def bulk_attendance():
    """Mark attendance for multiple trainees"""
    return AttendanceController.bulk_attendance()

@attendance_bp.route('/session/<int:session_id>', methods=['GET'])
@login_required
@require_module('attendance')
def get_session_attendance(session_id):
    """Get attendance for a specific session"""
    return AttendanceController.get_session_attendance(session_id)

@attendance_bp.route('/trainee/<int:trainee_id>', methods=['GET'])
@login_required
@require_module('attendance')
def get_trainee_attendance(trainee_id):
    """Get attendance for a specific trainee"""
    return AttendanceController.get_trainee_attendance(trainee_id)

@attendance_bp.route('/verify/<int:record_id>', methods=['POST'])
@login_required
@require_module('attendance')
def verify_attendance(record_id):
    """Verify an attendance record"""
    return AttendanceController.verify_attendance(record_id)

@attendance_bp.route('/stats', methods=['GET'])
@login_required
@require_module('attendance')
def get_attendance_stats():
    """Get attendance statistics"""
    return AttendanceController.get_attendance_stats()
