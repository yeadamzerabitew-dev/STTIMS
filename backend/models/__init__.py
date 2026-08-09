# =============================================
# MODELS PACKAGE INITIALIZATION
# Short-Term Training Institution Management System
# =============================================

# =============================================
# IMPORT db FROM base.py (SINGLE SOURCE OF TRUTH)
# =============================================
from models.base import db

# =============================================
# Import All Models
# =============================================
from models.base import BaseModel
from models.user import User
from models.trainee import Trainee
from models.instructor import Instructor
from models.category import Category
from models.course import Course
from models.batch import Batch
from models.enrollment import Enrollment
from models.grade_scale import GradeScale
from models.class_session import ClassSession
from models.attendance import AttendanceRecord
from models.assessment import Assessment
from models.trainee_result import TraineeResult
from models.certificate import Certificate
from models.certificate_setting import CertificateSetting
from models.course_assignment import CourseAssignment
from models.emergency_contact import EmergencyContact
from models.instructor_specialization import InstructorSpecialization
from models.system_log import SystemLog
from models.notification import Notification
from models.setting import Setting  # <-- Added Setting model

# =============================================
# Export All Models
# =============================================
__all__ = [
    'db',
    'BaseModel',
    'User',
    'Trainee',
    'Instructor',
    'Category',
    'Course',
    'Batch',
    'Enrollment',
    'GradeScale',
    'ClassSession',
    'AttendanceRecord',
    'Assessment',
    'TraineeResult',
    'Certificate',
    'CertificateSetting',
    'CourseAssignment',
    'EmergencyContact',
    'InstructorSpecialization',
    'SystemLog',
    'Notification',
    'Setting'  # <-- Added Setting to exports
]

# =============================================
# Model Registry (Optional Helper)
# =============================================

def get_model(model_name):
    """
    Get a model class by name.
    
    Args:
        model_name (str): Name of the model (e.g., 'User', 'Trainee')
    
    Returns:
        Model class or None if not found
    """
    model_map = {
        'User': User,
        'Trainee': Trainee,
        'Instructor': Instructor,
        'Course': Course,
        'Category': Category,
        'Batch': Batch,
        'Enrollment': Enrollment,
        'GradeScale': GradeScale,
        'ClassSession': ClassSession,
        'AttendanceRecord': AttendanceRecord,
        'Assessment': Assessment,
        'TraineeResult': TraineeResult,
        'Certificate': Certificate,
        'CertificateSetting': CertificateSetting,
        'CourseAssignment': CourseAssignment,
        'EmergencyContact': EmergencyContact,
        'InstructorSpecialization': InstructorSpecialization,
        'SystemLog': SystemLog,
        'Notification': Notification,
        'Setting': Setting
    }
    return model_map.get(model_name)

def get_all_models():
    """
    Get a dictionary of all models.
    
    Returns:
        dict: Dictionary of model names to model classes
    """
    return {
        'User': User,
        'Trainee': Trainee,
        'Instructor': Instructor,
        'Course': Course,
        'Category': Category,
        'Batch': Batch,
        'Enrollment': Enrollment,
        'GradeScale': GradeScale,
        'ClassSession': ClassSession,
        'AttendanceRecord': AttendanceRecord,
        'Assessment': Assessment,
        'TraineeResult': TraineeResult,
        'Certificate': Certificate,
        'CertificateSetting': CertificateSetting,
        'CourseAssignment': CourseAssignment,
        'EmergencyContact': EmergencyContact,
        'InstructorSpecialization': InstructorSpecialization,
        'SystemLog': SystemLog,
        'Notification': Notification,
        'Setting': Setting
    }

def get_model_count():
    """
    Get the total number of models.
    
    Returns:
        int: Number of models
    """
    return len(get_all_models())

def get_models_with_relationships():
    """
    Get a dictionary of models with their relationships.
    
    Returns:
        dict: Dictionary of model names to relationship lists
    """
    return {
        'User': ['trainee_profile', 'instructor_profile', 'logs', 'notifications', 
                 'approved_certificates', 'created_assessments', 'created_assignments',
                 'recorded_attendance', 'recorded_results'],
        'Trainee': ['user', 'emergency_contacts', 'attendance_records', 'trainee_results', 'enrollments'],
        'Instructor': ['user', 'specializations', 'course_assignments', 'class_sessions'],
        'Course': ['category', 'batches', 'certificate_settings'],
        'Category': ['subcategories', 'parent_category', 'courses'],
        'Batch': ['course', 'enrollments', 'sessions', 'assessments', 'course_assignments'],
        'Enrollment': ['trainee', 'batch', 'certificate'],
        'ClassSession': ['batch', 'instructor', 'attendance_records'],
        'Assessment': ['batch', 'results', 'creator'],
        'TraineeResult': ['assessment', 'trainee', 'recorder'],
        'Certificate': ['enrollment', 'template', 'approved_by_user'],
        'CertificateSetting': ['course', 'certificates'],
        'CourseAssignment': ['instructor', 'batch', 'creator'],
        'AttendanceRecord': ['session', 'trainee', 'recorder'],
        'SystemLog': ['user'],
        'Notification': ['user'],
        'Setting': []  # No relationships
    }

# =============================================
# Module Information
# =============================================
__version__ = '1.0.0'
__author__ = 'STTIMS Team'
__description__ = 'Database models for Short-Term Training Institution Management System'
