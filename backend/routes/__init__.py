from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.trainee_routes import trainee_bp
from routes.instructor_routes import instructor_bp
from routes.category_routes import category_bp
from routes.course_routes import course_bp
from routes.batch_routes import batch_bp
from routes.enrollment_routes import enrollment_bp
from routes.session_routes import session_bp
from routes.attendance_routes import attendance_bp
from routes.assessment_routes import assessment_bp
from routes.result_routes import result_bp
from routes.certificate_routes import certificate_bp
from routes.report_routes import report_bp
from routes.dashboard_routes import dashboard_bp
from routes.settings_routes import settings_bp

__all__ = [
    'auth_bp',
    'user_bp',
    'trainee_bp',
    'instructor_bp',
    'category_bp',
    'course_bp',
    'batch_bp',
    'enrollment_bp',
    'session_bp',
    'attendance_bp',
    'assessment_bp',
    'result_bp',
    'certificate_bp',
    'report_bp',
    'dashboard_bp',
    'settings_bp'
]
