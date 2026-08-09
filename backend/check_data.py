from app import app
from models import (
    db, User, Trainee, Instructor, Category, Course, Batch,
    Enrollment, GradeScale, ClassSession, AttendanceRecord, Assessment,
    TraineeResult, Certificate, CertificateSetting, CourseAssignment,
    EmergencyContact, InstructorSpecialization, SystemLog, Notification, Setting
)

models_to_check = [
    ('Users', User), ('Trainees', Trainee), ('Instructors', Instructor),
    ('Categories', Category), ('Courses', Course), ('Batches', Batch),
    ('Enrollments', Enrollment), ('GradeScale', GradeScale),
    ('ClassSessions', ClassSession), ('AttendanceRecords', AttendanceRecord),
    ('Assessments', Assessment), ('TraineeResults', TraineeResult),
    ('Certificates', Certificate), ('CertificateSettings', CertificateSetting),
    ('CourseAssignments', CourseAssignment), ('EmergencyContacts', EmergencyContact),
    ('InstructorSpecializations', InstructorSpecialization),
    ('SystemLogs', SystemLog), ('Notifications', Notification), ('Setting', Setting),
]

with app.app_context():
    print(f"{'Table':<28}{'Row Count':>10}")
    print("-" * 38)
    for name, model in models_to_check:
        try:
            count = model.query.count()
            print(f"{name:<28}{count:>10}")
        except Exception as e:
            print(f"{name:<28}{'ERROR: ' + str(e)[:60]}")
