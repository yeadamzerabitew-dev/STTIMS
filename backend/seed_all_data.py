#!/usr/bin/env python
"""Complete data seeding for STTIMS - Populates all tables with sample data"""

from app import app
from models import db, User, Trainee, Instructor, Course, Category, Batch, Enrollment, ClassSession, AttendanceRecord, Assessment, TraineeResult, Certificate, GradeScale, Setting
from datetime import datetime, timedelta
import random
import hashlib

def seed_all_data():
    with app.app_context():
        print("=" * 60)
        print("📊 STTIMS - Complete Data Seeding")
        print("=" * 60)
        
        # Check if data already exists
        if User.query.count() > 1:
            print("⚠️ Data already exists! Skipping...")
            return
        
        print("📁 Creating data...")
        
        # =============================================
        # 1. Create Users (if not exists)
        # =============================================
        print("👤 Creating users...")
        users_data = [
            {'username': 'admin', 'email': 'admin@sttims.com', 'role': 'Admin', 'password': 'Admin123!'},
            {'username': 'manager', 'email': 'manager@sttims.com', 'role': 'Manager', 'password': 'Manager123!'},
            {'username': 'instructor', 'email': 'instructor@sttims.com', 'role': 'Instructor', 'password': 'Instructor123!'},
            {'username': 'trainee', 'email': 'trainee@sttims.com', 'role': 'Trainee', 'password': 'Trainee123!'},
        ]
        
        users = []
        for u in users_data:
            existing = User.query.filter_by(username=u['username']).first()
            if not existing:
                user = User(
                    username=u['username'],
                    email=u['email'],
                    role=u['role'],
                    status='Active'
                )
                user.set_password(u['password'])
                db.session.add(user)
                users.append(user)
            else:
                users.append(existing)
        db.session.commit()
        print(f"✅ Created/Found {len(users)} users")

        # =============================================
        # 2. Create Categories
        # =============================================
        print("📁 Creating categories...")
        categories_data = [
            {'name': 'Information Technology', 'code': 'IT'},
            {'name': 'Business Management', 'code': 'BUS'},
            {'name': 'Data Science', 'code': 'DS'},
            {'name': 'Software Engineering', 'code': 'SE'},
            {'name': 'Networking', 'code': 'NET'},
            {'name': 'Cybersecurity', 'code': 'CS'},
            {'name': 'Cloud Computing', 'code': 'CLOUD'},
            {'name': 'Artificial Intelligence', 'code': 'AI'},
        ]
        
        categories = []
        for cat_data in categories_data:
            existing = Category.query.filter_by(category_code=cat_data['code']).first()
            if not existing:
                cat = Category(
                    category_name=cat_data['name'],
                    category_code=cat_data['code'],
                    description=f'Courses in {cat_data["name"]}',
                    status='Active'
                )
                db.session.add(cat)
                categories.append(cat)
            else:
                categories.append(existing)
        db.session.commit()
        print(f"✅ Created/Found {len(categories)} categories")

        # =============================================
        # 3. Create Courses
        # =============================================
        print("📚 Creating courses...")
        courses_data = [
            {'code': 'PY101', 'title': 'Python Programming', 'cat': 'IT', 'hours': 40, 'fee': 1500, 'capacity': 25, 'level': 'Beginner'},
            {'code': 'PY201', 'title': 'Advanced Python', 'cat': 'IT', 'hours': 45, 'fee': 2000, 'capacity': 20, 'level': 'Intermediate'},
            {'code': 'JS101', 'title': 'JavaScript Fundamentals', 'cat': 'IT', 'hours': 35, 'fee': 1200, 'capacity': 30, 'level': 'Beginner'},
            {'code': 'SQL101', 'title': 'SQL Database Design', 'cat': 'IT', 'hours': 30, 'fee': 1000, 'capacity': 20, 'level': 'Beginner'},
            {'code': 'DS101', 'title': 'Data Science Intro', 'cat': 'DS', 'hours': 45, 'fee': 2000, 'capacity': 15, 'level': 'Beginner'},
            {'code': 'ML101', 'title': 'Machine Learning', 'cat': 'DS', 'hours': 50, 'fee': 2500, 'capacity': 15, 'level': 'Intermediate'},
            {'code': 'BUS101', 'title': 'Business Management', 'cat': 'BUS', 'hours': 30, 'fee': 800, 'capacity': 35, 'level': 'Beginner'},
            {'code': 'SE101', 'title': 'Software Engineering', 'cat': 'SE', 'hours': 40, 'fee': 1800, 'capacity': 20, 'level': 'Intermediate'},
            {'code': 'NET101', 'title': 'Network Fundamentals', 'cat': 'NET', 'hours': 35, 'fee': 1200, 'capacity': 20, 'level': 'Beginner'},
            {'code': 'CS101', 'title': 'Cybersecurity Basics', 'cat': 'CS', 'hours': 40, 'fee': 1600, 'capacity': 20, 'level': 'Beginner'},
            {'code': 'CLOUD101', 'title': 'Cloud Computing', 'cat': 'CLOUD', 'hours': 35, 'fee': 1500, 'capacity': 20, 'level': 'Beginner'},
            {'code': 'AI101', 'title': 'AI Fundamentals', 'cat': 'AI', 'hours': 45, 'fee': 2200, 'capacity': 15, 'level': 'Intermediate'},
        ]
        
        courses = []
        for c in courses_data:
            category = next((cat for cat in categories if cat.category_code == c['cat']), None)
            if category:
                existing = Course.query.filter_by(course_code=c['code']).first()
                if not existing:
                    course = Course(
                        course_code=c['code'],
                        course_title=c['title'],
                        category_id=category.category_id,
                        description=f'Learn {c["title"]}',
                        duration_hours=c['hours'],
                        fee_amount=c['fee'],
                        max_capacity=c['capacity'],
                        course_level=c['level'],
                        status='Active'
                    )
                    db.session.add(course)
                    courses.append(course)
                else:
                    courses.append(existing)
        db.session.commit()
        print(f"✅ Created/Found {len(courses)} courses")

        # =============================================
        # 4. Create Trainees
        # =============================================
        print("👨‍🎓 Creating trainees...")
        trainees_data = [
            ('T001', 'John', 'Doe', 'john.doe@email.com', '0912345678', 'Male', 'BSc'),
            ('T002', 'Jane', 'Smith', 'jane.smith@email.com', '0912345679', 'Female', 'MSc'),
            ('T003', 'Bob', 'Johnson', 'bob.johnson@email.com', '0912345680', 'Male', 'Diploma'),
            ('T004', 'Alice', 'Williams', 'alice.williams@email.com', '0912345681', 'Female', 'BSc'),
            ('T005', 'Charlie', 'Brown', 'charlie.brown@email.com', '0912345682', 'Male', 'High School'),
            ('T006', 'Diana', 'Jones', 'diana.jones@email.com', '0912345683', 'Female', 'MSc'),
            ('T007', 'Eve', 'Davis', 'eve.davis@email.com', '0912345684', 'Female', 'BSc'),
            ('T008', 'Frank', 'Miller', 'frank.miller@email.com', '0912345685', 'Male', 'Diploma'),
            ('T009', 'Grace', 'Wilson', 'grace.wilson@email.com', '0912345686', 'Female', 'BSc'),
            ('T010', 'Henry', 'Moore', 'henry.moore@email.com', '0912345687', 'Male', 'High School'),
            ('T011', 'Ivy', 'Taylor', 'ivy.taylor@email.com', '0912345688', 'Female', 'MSc'),
            ('T012', 'Jack', 'Anderson', 'jack.anderson@email.com', '0912345689', 'Male', 'BSc'),
            ('T013', 'Karen', 'Thomas', 'karen.thomas@email.com', '0912345690', 'Female', 'Diploma'),
            ('T014', 'Leo', 'Jackson', 'leo.jackson@email.com', '0912345691', 'Male', 'BSc'),
            ('T015', 'Mia', 'White', 'mia.white@email.com', '0912345692', 'Female', 'High School'),
        ]
        
        trainees = []
        for code, first, last, email, phone, gender, edu in trainees_data:
            existing = Trainee.query.filter_by(trainee_code=code).first()
            if not existing:
                trainee = Trainee(
                    trainee_code=code,
                    first_name=first,
                    last_name=last,
                    email=email,
                    phone_number=phone,
                    gender=gender,
                    date_of_birth=datetime(1990 + random.randint(0, 10), random.randint(1, 12), random.randint(1, 28)),
                    educational_level=edu,
                    emergency_contact_name=f'{first} {last} Sr.',
                    emergency_contact_phone=f'09{random.randint(10000000, 99999999)}',
                    status='Active'
                )
                db.session.add(trainee)
                trainees.append(trainee)
            else:
                trainees.append(existing)
        db.session.commit()
        print(f"✅ Created/Found {len(trainees)} trainees")

        # =============================================
        # 5. Create Instructors
        # =============================================
        print("👨‍🏫 Creating instructors...")
        instructors_data = [
            ('INS001', 'Dr. Sarah', 'Smith', 'sarah.smith@sttims.com', '0912345700', 'Female', 'PhD Computer Science', 12, 'IT'),
            ('INS002', 'Prof. James', 'Wilson', 'james.wilson@sttims.com', '0912345701', 'Male', 'PhD Data Science', 15, 'DS'),
            ('INS003', 'Dr. Maria', 'Garcia', 'maria.garcia@sttims.com', '0912345702', 'Female', 'MBA Business', 10, 'BUS'),
            ('INS004', 'Prof. Robert', 'Taylor', 'robert.taylor@sttims.com', '0912345703', 'Male', 'MS Software Engineering', 18, 'SE'),
            ('INS005', 'Dr. Emily', 'Brown', 'emily.brown@sttims.com', '0912345704', 'Female', 'PhD Networking', 8, 'NET'),
            ('INS006', 'Prof. David', 'Lee', 'david.lee@sttims.com', '0912345705', 'Male', 'PhD Cybersecurity', 10, 'CS'),
            ('INS007', 'Dr. Lisa', 'Wang', 'lisa.wang@sttims.com', '0912345706', 'Female', 'PhD Cloud Computing', 7, 'CLOUD'),
            ('INS008', 'Prof. Michael', 'Chen', 'michael.chen@sttims.com', '0912345707', 'Male', 'PhD Artificial Intelligence', 9, 'AI'),
        ]
        
        instructors = []
        for code, first, last, email, phone, gender, qual, exp, dept in instructors_data:
            existing = Instructor.query.filter_by(instructor_code=code).first()
            if not existing:
                instructor = Instructor(
                    instructor_code=code,
                    first_name=first,
                    last_name=last,
                    email=email,
                    phone_number=phone,
                    gender=gender,
                    date_of_birth=datetime(1970 + random.randint(0, 15), random.randint(1, 12), random.randint(1, 28)),
                    qualification=qual,
                    years_of_experience=exp,
                    employment_type='Full Time',
                    joining_date=datetime(2010 + random.randint(0, 10), random.randint(1, 12), random.randint(1, 28)),
                    department=dept,
                    status='Active'
                )
                db.session.add(instructor)
                instructors.append(instructor)
            else:
                instructors.append(existing)
        db.session.commit()
        print(f"✅ Created/Found {len(instructors)} instructors")

        # =============================================
        # 6. Create Batches
        # =============================================
        print("📦 Creating batches...")
        batch_names = ['Morning', 'Evening', 'Weekend', 'Intensive', 'Online']
        schedule_types = ['Weekday', 'Evening', 'Weekend', 'Intensive', 'Online']
        
        batches = []
        for i, course in enumerate(courses[:10]):
            instructor = instructors[i % len(instructors)]
            for j in range(2):
                start_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
                end_date = start_date + timedelta(days=30 + random.randint(0, 15))
                
                batch_code = f"B{str(i+1).zfill(2)}{str(j+1).zfill(2)}"
                existing = Batch.query.filter_by(batch_code=batch_code).first()
                
                if not existing:
                    batch = Batch(
                        batch_code=batch_code,
                        batch_name=f"{course.course_title} - {batch_names[j % len(batch_names)]}",
                        course_id=course.course_id,
                        start_date=start_date,
                        end_date=end_date,
                        schedule_type=schedule_types[j % len(schedule_types)],
                        max_capacity=15 + random.randint(0, 15),
                        current_enrollment=random.randint(5, 15),
                        status=random.choices(['Upcoming', 'Ongoing', 'Completed'], weights=[30, 50, 20])[0],
                        instructor_id=instructor.instructor_id
                    )
                    db.session.add(batch)
                    batches.append(batch)
                else:
                    batches.append(existing)
        db.session.commit()
        print(f"✅ Created/Found {len(batches)} batches")

        # =============================================
        # 7. Create Enrollments
        # =============================================
        print("📝 Creating enrollments...")
        enrollments = []
        for trainee in trainees:
            num_batches = random.randint(1, min(3, len(batches)))
            selected_batches = random.sample(batches, num_batches)
            
            for batch in selected_batches:
                # Check if already enrolled
                existing = Enrollment.query.filter_by(
                    trainee_id=trainee.trainee_id,
                    batch_id=batch.batch_id
                ).first()
                
                if not existing:
                    status = random.choices(['Active', 'Completed', 'Dropped'], weights=[60, 30, 10])[0]
                    payment_status = random.choices(['Paid', 'Pending', 'Partial'], weights=[60, 25, 15])[0]
                    
                    enrollment = Enrollment(
                        trainee_id=trainee.trainee_id,
                        batch_id=batch.batch_id,
                        enrollment_date=datetime.now() - timedelta(days=random.randint(0, 30)),
                        status=status,
                        payment_status=payment_status
                    )
                    db.session.add(enrollment)
                    enrollments.append(enrollment)
        db.session.commit()
        print(f"✅ Created {len(enrollments)} enrollments")

        # =============================================
        # 8. Create Class Sessions
        # =============================================
        print("🕐 Creating class sessions...")
        sessions = []
        for batch in batches[:15]:
            if batch.status != 'Cancelled':
                num_sessions = random.randint(5, 10)
                for i in range(num_sessions):
                    session_date = batch.start_date + timedelta(days=i*2)
                    if session_date <= batch.end_date:
                        session = ClassSession(
                            batch_id=batch.batch_id,
                            session_date=session_date,
                            start_time='09:00:00',
                            end_time='12:00:00',
                            topic_covered=f'Session {i+1}: {random.choice(["Introduction", "Basics", "Advanced", "Practice", "Review", "Project Work"])}',
                            session_type=random.choice(['Lecture', 'Lab', 'Workshop', 'Practical']),
                            instructor_id=batch.instructor_id,
                            status='Completed' if session_date < datetime.now().date() else 'Scheduled'
                        )
                        db.session.add(session)
                        sessions.append(session)
        db.session.commit()
        print(f"✅ Created {len(sessions)} class sessions")

        # =============================================
        # 9. Create Attendance Records
        # =============================================
        print("📋 Creating attendance records...")
        attendance_records = []
        for session in sessions[:40]:
            # Get enrollments for this batch
            batch_enrollments = Enrollment.query.filter_by(batch_id=session.batch_id).all()
            for enrollment in batch_enrollments[:8]:
                status = random.choices(['Present', 'Absent', 'Late', 'Excused'], weights=[70, 15, 10, 5])[0]
                record = AttendanceRecord(
                    session_id=session.session_id,
                    trainee_id=enrollment.trainee_id,
                    status=status,
                    check_in_time='09:00:00' if status == 'Present' else None,
                    check_out_time='12:00:00' if status == 'Present' else None,
                    is_verified=random.choice([True, False])
                )
                db.session.add(record)
                attendance_records.append(record)
        db.session.commit()
        print(f"✅ Created {len(attendance_records)} attendance records")

        # =============================================
        # 10. Create Assessments
        # =============================================
        print("📝 Creating assessments...")
        assessments = []
        assessment_types = ['Quiz', 'Assignment', 'Lab', 'Project', 'Exam', 'Practical']
        for batch in batches[:10]:
            num_assessments = random.randint(2, 4)
            for i in range(num_assessments):
                assessment = Assessment(
                    batch_id=batch.batch_id,
                    title=f"{assessment_types[i % len(assessment_types)]} {i+1}",
                    assessment_type=assessment_types[i % len(assessment_types)],
                    max_marks=random.randint(50, 100),
                    weightage_percent=random.randint(10, 30),
                    assessment_date=datetime.now().date() + timedelta(days=random.randint(1, 20)),
                    status=random.choice(['Scheduled', 'Completed'])
                )
                db.session.add(assessment)
                assessments.append(assessment)
        db.session.commit()
        print(f"✅ Created {len(assessments)} assessments")

        # =============================================
        # 11. Create Trainee Results
        # =============================================
        print("📊 Creating trainee results...")
        results = []
        for assessment in assessments[:30]:
            enrollments_for_batch = Enrollment.query.filter_by(batch_id=assessment.batch_id).all()
            for enrollment in enrollments_for_batch[:6]:
                marks = random.randint(0, assessment.max_marks)
                percentage = (marks / assessment.max_marks) * 100
                grade = 'A' if percentage >= 85 else 'B' if percentage >= 70 else 'C' if percentage >= 50 else 'F'
                status = 'Pass' if percentage >= 50 else 'Fail'
                
                result = TraineeResult(
                    assessment_id=assessment.assessment_id,
                    trainee_id=enrollment.trainee_id,
                    marks_obtained=marks,
                    percentage_score=percentage,
                    grade=grade,
                    status=status
                )
                db.session.add(result)
                results.append(result)
        db.session.commit()
        print(f"✅ Created {len(results)} trainee results")

        # =============================================
        # 12. Create Certificates
        # =============================================
        print("🎓 Creating certificates...")
        completed_enrollments = Enrollment.query.filter_by(status='Completed').all()
        certificates = []
        for enrollment in completed_enrollments[:12]:
            certificate = Certificate(
                enrollment_id=enrollment.enrollment_id,
                certificate_number=f"CERT-{datetime.now().year()}-{str(enrollment.enrollment_id).zfill(5)}",
                issue_date=datetime.now(),
                status='Issued',
                verification_token=f"VERIFY-{datetime.now().year()}-{random.randint(10000, 99999)}"
            )
            db.session.add(certificate)
            certificates.append(certificate)
        db.session.commit()
        print(f"✅ Created {len(certificates)} certificates")

        # =============================================
        # 13. Create Grade Scale
        # =============================================
        print("📊 Creating grade scale...")
        if GradeScale.query.count() == 0:
            grades_data = [
                {'letter': 'A', 'point': 4.0, 'min': 85, 'max': 100, 'desc': 'Excellent', 'pass': True, 'order': 1},
                {'letter': 'A-', 'point': 3.7, 'min': 80, 'max': 84, 'desc': 'Very Good', 'pass': True, 'order': 2},
                {'letter': 'B+', 'point': 3.3, 'min': 75, 'max': 79, 'desc': 'Good', 'pass': True, 'order': 3},
                {'letter': 'B', 'point': 3.0, 'min': 70, 'max': 74, 'desc': 'Above Average', 'pass': True, 'order': 4},
                {'letter': 'B-', 'point': 2.7, 'min': 65, 'max': 69, 'desc': 'Average', 'pass': True, 'order': 5},
                {'letter': 'C+', 'point': 2.3, 'min': 60, 'max': 64, 'desc': 'Below Average', 'pass': True, 'order': 6},
                {'letter': 'C', 'point': 2.0, 'min': 55, 'max': 59, 'desc': 'Satisfactory', 'pass': True, 'order': 7},
                {'letter': 'C-', 'point': 1.7, 'min': 50, 'max': 54, 'desc': 'Passing', 'pass': True, 'order': 8},
                {'letter': 'D', 'point': 1.0, 'min': 45, 'max': 49, 'desc': 'Poor', 'pass': True, 'order': 9},
                {'letter': 'F', 'point': 0.0, 'min': 0, 'max': 44, 'desc': 'Fail', 'pass': False, 'order': 10},
            ]
            
            for g in grades_data:
                grade = GradeScale(
                    grade_letter=g['letter'],
                    grade_point=g['point'],
                    min_percentage=g['min'],
                    max_percentage=g['max'],
                    description=g['desc'],
                    is_pass=g['pass'],
                    display_order=g['order']
                )
                db.session.add(grade)
            db.session.commit()
            print("✅ Grade scale created!")
        else:
            print("⚠️ Grade scale already exists")

        # =============================================
        # 14. Create Settings
        # =============================================
        print("⚙️ Creating settings...")
        if Setting.query.count() == 0:
            settings = Setting()
            db.session.add(settings)
            db.session.commit()
            print("✅ Settings created!")
        else:
            print("⚠️ Settings already exist")

        # =============================================
        # Summary
        # =============================================
        print("\n" + "=" * 60)
        print("✅ Data seeding completed successfully!")
        print("=" * 60)
        print("📊 Data Summary:")
        print(f"  Users: {User.query.count()}")
        print(f"  Categories: {Category.query.count()}")
        print(f"  Courses: {Course.query.count()}")
        print(f"  Trainees: {Trainee.query.count()}")
        print(f"  Instructors: {Instructor.query.count()}")
        print(f"  Batches: {Batch.query.count()}")
        print(f"  Enrollments: {Enrollment.query.count()}")
        print(f"  Class Sessions: {ClassSession.query.count()}")
        print(f"  Attendance Records: {AttendanceRecord.query.count()}")
        print(f"  Assessments: {Assessment.query.count()}")
        print(f"  Trainee Results: {TraineeResult.query.count()}")
        print(f"  Certificates: {Certificate.query.count()}")
        print(f"  Grade Scale: {GradeScale.query.count()}")
        print(f"  Settings: {Setting.query.count()}")
        print("=" * 60)
        print("🔑 Test Credentials:")
        print("  Admin:      admin / Admin123!")
        print("  Manager:    manager / Manager123!")
        print("  Instructor: instructor / Instructor123!")
        print("  Trainee:    trainee / Trainee123!")
        print("=" * 60)

if __name__ == '__main__':
    seed_all_data()
