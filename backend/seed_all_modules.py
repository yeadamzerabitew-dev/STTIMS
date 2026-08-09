from app import app
from models import db, User, Trainee, Instructor, Course, Category, Batch, Enrollment, ClassSession, AttendanceRecord, GradeScale, CourseAssignment, Assessment, TraineeResult, Certificate
from datetime import datetime, date, timedelta

def seed():
    with app.app_context():
        print("🚀 Starting Full System Seeding...")
        
        # 0. Clear existing data to avoid duplicates
        db.drop_all()
        db.create_all()

        # 1. Grade Scale (Needed for Results)
        grades = [
            ('A', 4.0, 85, 100, 'Excellent'), 
            ('B', 3.0, 70, 84, 'Good'), 
            ('C', 2.0, 50, 69, 'Satisfactory'), 
            ('F', 0.0, 0, 49, 'Fail')
        ]
        for let, pt, mi, ma, desc in grades:
            db.session.add(GradeScale(grade_letter=let, grade_point=pt, min_percentage=mi, max_percentage=ma, description=desc, is_pass=(let!='F')))

        # 2. Categories
        it = Category(category_name='Information Technology', category_code='IT', status='Active')
        biz = Category(category_name='Business', category_code='BIZ', status='Active')
        db.session.add_all([it, biz])
        db.session.flush()

        # 3. Courses
        python_course = Course(course_code='PY101', course_title='Python for Beginners', category_id=it.category_id, duration_hours=40, fee_amount=2500, max_capacity=30, status='Active', description='Basic Python programming.')
        excel_course = Course(course_code='EX101', course_title='Advanced Excel', category_id=biz.category_id, duration_hours=20, fee_amount=1500, max_capacity=20, status='Active', description='Mastering Spreadsheets.')
        db.session.add_all([python_course, excel_course])
        db.session.flush()

        # 4. Trainees (Adding 3 Trainees)
        t_data = [
            ('T001', 'Abebe', 'Bikila', 'abebe@test.com', '0911000001'),
            ('T002', 'Martha', 'Tadesse', 'martha@test.com', '0911000002'),
            ('T003', 'John', 'Smith', 'john@test.com', '0911000003')
        ]
        trainees = []
        for code, f, l, em, ph in t_data:
            t = Trainee(trainee_code=code, first_name=f, last_name=l, email=em, phone_number=ph, gender='Male' if f=='John' else 'Female', date_of_birth=date(1998,5,5), educational_level='Degree', emergency_contact_name='Parent', emergency_contact_phone='09000000', status='Active')
            db.session.add(t)
            trainees.append(t)
        db.session.flush()

        # 5. Instructors (Adding 2 Instructors)
        i_data = [
            ('INS01', 'Dr. Elias', 'Tesfaye', 'elias@sttims.com'),
            ('INS02', 'Sara', 'Girma', 'sara@sttims.com')
        ]
        instructors = []
        for code, f, l, em in i_data:
            ins = Instructor(instructor_code=code, first_name=f, last_name=l, email=em, phone_number='0922000000', gender='Male' if f=='Dr. Elias' else 'Female', date_of_birth=date(1985,1,1), qualification='Masters', employment_type='Full Time', joining_date=date.today(), status='Active')
            db.session.add(ins)
            instructors.append(ins)
        db.session.flush()

        # 6. Users (Admin + Staff + Trainees)
        admin = User(username='admin', email='admin@sttims.com', role='Admin', status='Active')
        admin.set_password('Admin123!')
        
        manager = User(username='manager', email='manager@sttims.com', role='Manager', status='Active')
        manager.set_password('Manager123!')
        
        db.session.add_all([admin, manager])
        
        # Create user accounts for trainees
        for i, t in enumerate(trainees):
            u = User(username=f'trainee{i+1}', email=t.email, role='Trainee', status='Active', trainee_id=t.trainee_id)
            u.set_password('Trainee123!')
            db.session.add(u)
        db.session.flush()

        # 7. Batches (2 Batches)
        b1 = Batch(batch_code='B01', batch_name='Python Morning', course_id=python_course.course_id, start_date=date.today()-timedelta(days=10), end_date=date.today()+timedelta(days=20), schedule_type='Weekday', max_capacity=20, status='Ongoing')
        b2 = Batch(batch_code='B02', batch_name='Excel Evening', course_id=excel_course.course_id, start_date=date.today()+timedelta(days=5), end_date=date.today()+timedelta(days=35), schedule_type='Evening', max_capacity=15, status='Upcoming')
        db.session.add_all([b1, b2])
        db.session.flush()

        # 8. Course Assignments
        db.session.add(CourseAssignment(instructor_id=instructors[0].instructor_id, batch_id=b1.batch_id, assignment_date=date.today(), role='Primary Instructor', start_date=b1.start_date, end_date=b1.end_date, status='Active', created_by=admin.user_id))
        db.session.add(CourseAssignment(instructor_id=instructors[1].instructor_id, batch_id=b2.batch_id, assignment_date=date.today(), role='Primary Instructor', start_date=b2.start_date, end_date=b2.end_date, status='Active', created_by=admin.user_id))

        # 9. Enrollments (Link Trainees to Batches)
        enr1 = Enrollment(enrollment_number='E001', trainee_id=trainees[0].trainee_id, batch_id=b1.batch_id, status='Active', payment_status='Paid', payment_amount=2500, final_amount=2500)
        enr2 = Enrollment(enrollment_number='E002', trainee_id=trainees[1].trainee_id, batch_id=b1.batch_id, status='Active', payment_status='Partial', payment_amount=1000, final_amount=2500)
        db.session.add_all([enr1, enr2])
        db.session.flush()

        # 10. Class Sessions & Attendance
        session = ClassSession(session_code='S01', batch_id=b1.batch_id, session_date=date.today()-timedelta(days=1), start_time=datetime.now().time(), end_time=datetime.now().time(), topic_covered='Loops', session_type='Lecture', instructor_id=instructors[0].instructor_id, status='Completed')
        db.session.add(session)
        db.session.flush()
        
        # Mark Attendance for the session
        db.session.add(AttendanceRecord(session_id=session.session_id, trainee_id=trainees[0].trainee_id, status='Present', recorded_by=admin.user_id))
        db.session.add(AttendanceRecord(session_id=session.session_id, trainee_id=trainees[1].trainee_id, status='Absent', recorded_by=admin.user_id))

        # 11. Assessments & Results
        quiz = Assessment(assessment_code='Q1', batch_id=b1.batch_id, title='Python Basics Quiz', assessment_type='Quiz', max_marks=100, weightage_percent=20, assessment_date=date.today()-timedelta(days=2), status='Completed', created_by=admin.user_id)
        db.session.add(quiz)
        db.session.flush()
        
        # Add a Result for Trainee 1
        res = TraineeResult(assessment_id=quiz.assessment_id, trainee_id=trainees[0].trainee_id, marks_obtained=90, percentage_score=90, grade='A', status='Pass', recorded_by=admin.user_id)
        db.session.add(res)

        # 12. Certificates (Generating one for a "Completed" test)
        # Note: Usually generated after course end, but we'll add one for testing.
        cert = Certificate(certificate_number='CERT-001', enrollment_id=enr1.enrollment_id, issue_date=date.today(), status='Issued', verification_token='ABC-123', approved_by=admin.user_id)
        db.session.add(cert)

        db.session.commit()
        print("✅ ALL MODULES SEEDED SUCCESSFULLY!")

if __name__ == '__main__':
    seed()
