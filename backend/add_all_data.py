#!/usr/bin/env python
"""Add complete sample data to STTIMS database"""

from app import app
from models import db, User, Trainee, Instructor, Course, Category, Batch, Enrollment, Certificate, ClassSession, Assessment, TraineeResult, AttendanceRecord
from datetime import datetime, timedelta
import random

def add_all_data():
    with app.app_context():
        print("📊 Adding complete sample data to STTIMS...")
        
        # Check if data already exists
        if Trainee.query.count() > 0 and Batch.query.count() > 0:
            print("⚠️ Data already exists. Skipping...")
            return
        
        # =============================================
        # 1. Create Categories (if not exists)
        # =============================================
        print("📁 Creating categories...")
        categories_data = [
            {'name': 'Information Technology', 'code': 'IT'},
            {'name': 'Business Management', 'code': 'BUS'},
            {'name': 'Data Science', 'code': 'DS'},
            {'name': 'Software Engineering', 'code': 'SE'},
            {'name': 'Networking', 'code': 'NET'},
        ]
        
        categories = []
        for cat_data in categories_data:
            existing = Category.query.filter_by(category_code=cat_data['code']).first()
            if existing:
                categories.append(existing)
            else:
                cat = Category(
                    category_name=cat_data['name'],
                    category_code=cat_data['code'],
                    status='Active'
                )
                db.session.add(cat)
                categories.append(cat)
        db.session.commit()
        print(f"✅ Created/Found {len(categories)} categories")

        # =============================================
        # 2. Create Courses
        # =============================================
        print("📚 Creating courses...")
        courses_data = [
            {'code': 'PY101', 'title': 'Python Programming', 'cat': 'IT', 'hours': 40, 'fee': 1500, 'capacity': 20},
            {'code': 'JS101', 'title': 'JavaScript', 'cat': 'IT', 'hours': 35, 'fee': 1200, 'capacity': 25},
            {'code': 'SQL101', 'title': 'SQL Database', 'cat': 'IT', 'hours': 30, 'fee': 1000, 'capacity': 20},
            {'code': 'DS101', 'title': 'Data Science Intro', 'cat': 'DS', 'hours': 45, 'fee': 2000, 'capacity': 15},
            {'code': 'ML101', 'title': 'Machine Learning', 'cat': 'DS', 'hours': 50, 'fee': 2500, 'capacity': 15},
            {'code': 'BUS101', 'title': 'Business Management', 'cat': 'BUS', 'hours': 30, 'fee': 800, 'capacity': 30},
            {'code': 'SE101', 'title': 'Software Engineering', 'cat': 'SE', 'hours': 40, 'fee': 1800, 'capacity': 20},
            {'code': 'NET101', 'title': 'Network Fundamentals', 'cat': 'NET', 'hours': 35, 'fee': 1200, 'capacity': 20},
        ]
        
        courses = []
        for c in courses_data:
            category = next((cat for cat in categories if cat.category_code == c['cat']), None)
            if category:
                course = Course(
                    course_code=c['code'],
                    course_title=c['title'],
                    category_id=category.category_id,
                    description=f'Learn {c["title"]}',
                    duration_hours=c['hours'],
                    fee_amount=c['fee'],
                    max_capacity=c['capacity'],
                    status='Active'
                )
                db.session.add(course)
                courses.append(course)
        db.session.commit()
        print(f"✅ Created {len(courses)} courses")

        # =============================================
        # 3. Create Trainees
        # =============================================
        print("👨‍🎓 Creating trainees...")
        trainees_data = [
            ('T001', 'John', 'Doe', 'john@email.com', '0912345678', 'Male', 'BSc'),
            ('T002', 'Jane', 'Smith', 'jane@email.com', '0912345679', 'Female', 'MSc'),
            ('T003', 'Bob', 'Johnson', 'bob@email.com', '0912345680', 'Male', 'Diploma'),
            ('T004', 'Alice', 'Williams', 'alice@email.com', '0912345681', 'Female', 'BSc'),
            ('T005', 'Charlie', 'Brown', 'charlie@email.com', '0912345682', 'Male', 'High School'),
            ('T006', 'Diana', 'Jones', 'diana@email.com', '0912345683', 'Female', 'MSc'),
            ('T007', 'Eve', 'Davis', 'eve@email.com', '0912345684', 'Female', 'BSc'),
            ('T008', 'Frank', 'Miller', 'frank@email.com', '0912345685', 'Male', 'Diploma'),
        ]
        
        trainees = []
        for code, first, last, email, phone, gender, edu in trainees_data:
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
        db.session.commit()
        print(f"✅ Created {len(trainees)} trainees")

        # =============================================
        # 4. Create Instructors
        # =============================================
        print("👨‍🏫 Creating instructors...")
        instructors_data = [
            ('INS001', 'Dr. Sarah', 'Smith', 'sarah@email.com', '0912345690', 'Female', 'PhD CS', 10, 'IT'),
            ('INS002', 'Prof. James', 'Wilson', 'james@email.com', '0912345691', 'Male', 'PhD DS', 12, 'DS'),
            ('INS003', 'Dr. Maria', 'Garcia', 'maria@email.com', '0912345692', 'Female', 'MBA Business', 8, 'BUS'),
            ('INS004', 'Prof. Robert', 'Taylor', 'robert@email.com', '0912345693', 'Male', 'MS SE', 15, 'SE'),
        ]
        
        instructors = []
        for code, first, last, email, phone, gender, qual, exp, dept in instructors_data:
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
                joining_date=datetime(2015 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
                department=dept,
                status='Active'
            )
            db.session.add(instructor)
            instructors.append(instructor)
        db.session.commit()
        print(f"✅ Created {len(instructors)} instructors")

        # =============================================
        # 5. Create Batches
        # =============================================
        print("📦 Creating batches...")
        batch_names = ['Morning', 'Evening', 'Weekend']
        schedule_types = ['Weekday', 'Evening', 'Weekend']
        batches = []
        
        for i, course in enumerate(courses[:6]):
            instructor = instructors[i % len(instructors)]
            for j in range(2):
                start_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
                end_date = start_date + timedelta(days=30 + random.randint(0, 15))
                
                batch = Batch(
                    batch_code=f"B{str(i+1).zfill(2)}{str(j+1).zfill(2)}",
                    batch_name=f"{course.course_title} - {batch_names[j % len(batch_names)]}",
                    course_id=course.course_id,
                    start_date=start_date,
                    end_date=end_date,
                    schedule_type=schedule_types[j % len(schedule_types)],
                    max_capacity=15 + random.randint(0, 15),
                    current_enrollment=random.randint(5, 15),
                    status=random.choice(['Upcoming', 'Ongoing', 'Completed']),
                    instructor_id=instructor.instructor_id
                )
                db.session.add(batch)
                batches.append(batch)
        db.session.commit()
        print(f"✅ Created {len(batches)} batches")

        # =============================================
        # 6. Create Enrollments
        # =============================================
        print("📝 Creating enrollments...")
        enrollments = []
        for trainee in trainees:
            num_batches = random.randint(1, min(2, len(batches)))
            selected_batches = random.sample(batches, num_batches)
            
            for batch in selected_batches:
                status = random.choices(['Active', 'Completed', 'Dropped'], weights=[70, 20, 10])[0]
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
        # 7. Create Class Sessions
        # =============================================
        print("🕐 Creating class sessions...")
        sessions = []
        for batch in batches:
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
                            topic_covered=f'Session {i+1}: {random.choice(["Introduction", "Basics", "Advanced", "Practice", "Review"])}',
                            session_type=random.choice(['Lecture', 'Lab', 'Workshop']),
                            instructor_id=batch.instructor_id,
                            status='Completed' if session_date < datetime.now().date() else 'Scheduled'
                        )
                        db.session.add(session)
                        sessions.append(session)
        db.session.commit()
        print(f"✅ Created {len(sessions)} class sessions")

        # =============================================
        # 8. Create Attendance Records
        # =============================================
        print("📋 Creating attendance records...")
        attendance_records = []
        for session in sessions[:30]:  # Only first 30 sessions
            batch_enrollments = Enrollment.query.filter_by(batch_id=session.batch_id).all()
            for enrollment in batch_enrollments[:5]:  # First 5 trainees per session
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
        # 9. Create Assessments
        # =============================================
        print("📝 Creating assessments...")
        assessments = []
        assessment_types = ['Quiz', 'Assignment', 'Lab', 'Project', 'Exam', 'Practical']
        for batch in batches[:5]:
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
        # 10. Create Trainee Results
        # =============================================
        print("📊 Creating trainee results...")
        results = []
        for assessment in assessments[:20]:
            # Get enrolled trainees for this batch
            enrollments_for_batch = Enrollment.query.filter_by(batch_id=assessment.batch_id).all()
            for enrollment in enrollments_for_batch[:5]:  # First 5 trainees
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
        # 11. Create Certificates
        # =============================================
        print("🎓 Creating certificates...")
        completed_enrollments = Enrollment.query.filter_by(status='Completed').all()
        certificates = []
        for enrollment in completed_enrollments[:10]:
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
        # Summary
        # =============================================
        print("\n" + "=" * 60)
        print("✅ Complete sample data added successfully!")
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
        print("=" * 60)

if __name__ == '__main__':
    add_all_data()
