from app import app
from models import db, User, Trainee, Instructor, Course, Category, Batch, Enrollment, ClassSession, AttendanceRecord, GradeScale, CourseAssignment
from datetime import datetime, date, timedelta

def seed():
    with app.app_context():
        print("🌱 Seeding data via ORM...")

        # 1. Grade Scale
        grades = [
            ('A', 4.0, 85, 100), ('B', 3.0, 70, 84), ('C', 2.0, 50, 69), ('F', 0.0, 0, 49)
        ]
        for let, pt, mi, ma in grades:
            db.session.add(GradeScale(grade_letter=let, grade_point=pt, min_percentage=mi, max_percentage=ma, description='Grade', is_pass=(let!='F')))

        # 2. Categories
        it = Category(category_name='IT', category_code='IT', status='Active')
        biz = Category(category_name='Business', category_code='BIZ', status='Active')
        db.session.add_all([it, biz])
        db.session.flush()

        # 3. Courses
        py = Course(course_code='PY101', course_title='Python', category_id=it.category_id, duration_hours=40, fee_amount=2000, max_capacity=30, status='Active', description='Intro')
        db.session.add(py)
        db.session.flush()

        # 4. Trainee
        t1 = Trainee(trainee_code='T001', first_name='Abebe', last_name='Bikila', email='abebe@test.com', phone_number='0911223344', gender='Male', date_of_birth=date(1995,1,1), educational_level='BSc', emergency_contact_name='Contact', emergency_contact_phone='09000000', status='Active')
        db.session.add(t1)
        db.session.flush()

        # 5. Instructor
        ins = Instructor(instructor_code='INS01', first_name='Dr. Elias', last_name='Tesfaye', email='elias@sttims.com', phone_number='0988776655', gender='Male', date_of_birth=date(1980,1,1), qualification='PhD', employment_type='Full Time', joining_date=date.today(), status='Active')
        db.session.add(ins)
        db.session.flush()

        # 6. Admin User
        admin = User(username='admin', email='admin@sttims.com', role='Admin', status='Active')
        admin.set_password('Admin123!')
        db.session.add(admin)
        db.session.flush()

        # 7. Batch (Notice: instructor_id removed here)
        b1 = Batch(batch_code='B01', batch_name='Python Morning', course_id=py.course_id, start_date=date.today(), end_date=date.today()+timedelta(days=30), schedule_type='Weekday', max_capacity=20, status='Ongoing')
        db.session.add(b1)
        db.session.flush()

        # 8. Create Course Assignment (This is how your model links Instructors to Batches)
        assignment = CourseAssignment(
            instructor_id=ins.instructor_id,
            batch_id=b1.batch_id,
            assignment_date=date.today(),
            role='Primary Instructor',
            start_date=b1.start_date,
            end_date=b1.end_date,
            status='Active',
            created_by=admin.user_id # Admin created this assignment
        )
        db.session.add(assignment)

        # 9. Enrollment
        enr = Enrollment(enrollment_number='E001', trainee_id=t1.trainee_id, batch_id=b1.batch_id, status='Active', payment_status='Paid', payment_amount=2000, final_amount=2000)
        db.session.add(enr)
        
        db.session.commit()
        print("✅ Database Seeded Successfully with ORM and CourseAssignments!")

if __name__ == '__main__':
    seed()
