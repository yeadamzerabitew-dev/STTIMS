#!/usr/bin/env python3
"""
Insert sample data into STTIMS database using SQLAlchemy
This avoids SQL syntax issues and handles relationships properly
"""

from app import app
from models import db, User, Trainee, Instructor, Course, Category, Batch, Enrollment
from models import ClassSession, AttendanceRecord, Assessment, TraineeResult
from models import GradeScale, Certificate, CourseAssignment
from datetime import datetime, timedelta
import random

def insert_sample_data():
    with app.app_context():
        print("📊 Inserting sample data into STTIMS...")
        
        # Clear existing data (keep users)
        print("🧹 Clearing existing data...")
        try:
            db.session.execute('SET FOREIGN_KEY_CHECKS = 0')
            db.session.query(AttendanceRecord).delete()
            db.session.query(ClassSession).delete()
            db.session.query(TraineeResult).delete()
            db.session.query(Assessment).delete()
            db.session.query(Enrollment).delete()
            db.session.query(Batch).delete()
            db.session.query(CourseAssignment).delete()
            db.session.query(Certificate).delete()
            db.session.query(Trainee).delete()
            db.session.query(Instructor).delete()
            db.session.query(Course).delete()
            db.session.query(Category).delete()
            db.session.query(GradeScale).delete()
            db.session.execute('SET FOREIGN_KEY_CHECKS = 1')
            db.session.commit()
            print("✅ Data cleared")
        except Exception as e:
            print(f"⚠️  Could not clear all data: {e}")
            db.session.rollback()
        
        # 1. Insert Grade Scale
        print("📊 Inserting grade scale...")
        grades = [
            {'letter': 'A+', 'point': 4.00, 'min': 90.00, 'max': 100.00, 'desc': 'Exceptional', 'pass': True, 'order': 1},
            {'letter': 'A', 'point': 4.00, 'min': 85.00, 'max': 89.99, 'desc': 'Excellent', 'pass': True, 'order': 2},
            {'letter': 'A-', 'point': 3.75, 'min': 80.00, 'max': 84.99, 'desc': 'Very Good', 'pass': True, 'order': 3},
            {'letter': 'B+', 'point': 3.50, 'min': 75.00, 'max': 79.99, 'desc': 'Good Plus', 'pass': True, 'order': 4},
            {'letter': 'B', 'point': 3.00, 'min': 70.00, 'max': 74.99, 'desc': 'Good', 'pass': True, 'order': 5},
            {'letter': 'B-', 'point': 2.75, 'min': 65.00, 'max': 69.99, 'desc': 'Above Average', 'pass': True, 'order': 6},
            {'letter': 'C+', 'point': 2.50, 'min': 60.00, 'max': 64.99, 'desc': 'Average Plus', 'pass': True, 'order': 7},
            {'letter': 'C', 'point': 2.00, 'min': 55.00, 'max': 59.99, 'desc': 'Average', 'pass': True, 'order': 8},
            {'letter': 'C-', 'point': 1.75, 'min': 50.00, 'max': 54.99, 'desc': 'Below Average', 'pass': True, 'order': 9},
            {'letter': 'D', 'point': 1.00, 'min': 45.00, 'max': 49.99, 'desc': 'Marginal Pass', 'pass': True, 'order': 10},
            {'letter': 'F', 'point': 0.00, 'min': 0.00, 'max': 44.99, 'desc': 'Fail', 'pass': False, 'order': 11},
        ]
        
        for g in grades:
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
        print(f"✅ Inserted {len(grades)} grades")
        
        # 2. Insert Categories
        print("📂 Inserting categories...")
        categories_data = [
            {'name': 'Information Technology', 'code': 'IT', 'desc': 'Computer and IT Courses', 'icon': 'fa-laptop', 'order': 1},
            {'name': 'Electrical Engineering', 'code': 'EE', 'desc': 'Electrical and Electronics', 'icon': 'fa-bolt', 'order': 2},
            {'name': 'Mechanical Engineering', 'code': 'ME', 'desc': 'Mechanical Engineering', 'icon': 'fa-cogs', 'order': 3},
            {'name': 'Software Engineering', 'code': 'SE', 'desc': 'Software Development', 'icon': 'fa-code', 'order': 4},
            {'name': 'Data Science', 'code': 'DS', 'desc': 'Data Analytics & ML', 'icon': 'fa-database', 'order': 5},
            {'name': 'Business Management', 'code': 'BM', 'desc': 'Business Courses', 'icon': 'fa-briefcase', 'order': 6},
        ]
        
        for cat in categories_data:
            category = Category(
                category_name=cat['name'],
                category_code=cat['code'],
                description=cat['desc'],
                icon=cat['icon'],
                display_order=cat['order'],
                status='Active'
            )
            db.session.add(category)
        db.session.commit()
        categories = Category.query.all()
        print(f"✅ Inserted {len(categories)} categories")
        
        # 3. Insert Courses
        print("📚 Inserting courses...")
        courses_data = [
            {'code': 'C101', 'title': 'Python Programming Fundamentals', 'cat': 'IT', 'desc': 'Comprehensive Python programming course', 'hours': 40, 'fee': 2500.00, 'capacity': 30, 'level': 'Beginner'},
            {'code': 'C102', 'title': 'Electrical Safety and Standards', 'cat': 'EE', 'desc': 'Essential safety practices', 'hours': 30, 'fee': 1800.00, 'capacity': 25, 'level': 'Intermediate'},
            {'code': 'C103', 'title': 'Web Development with PHP', 'cat': 'SE', 'desc': 'Build dynamic websites', 'hours': 50, 'fee': 3500.00, 'capacity': 25, 'level': 'Intermediate'},
            {'code': 'C104', 'title': 'Project Management Fundamentals', 'cat': 'BM', 'desc': 'Essential project management skills', 'hours': 35, 'fee': 2000.00, 'capacity': 30, 'level': 'Beginner'},
            {'code': 'C105', 'title': 'Machine Learning Basics', 'cat': 'DS', 'desc': 'Introduction to ML concepts', 'hours': 45, 'fee': 4000.00, 'capacity': 20, 'level': 'Advanced'},
            {'code': 'C106', 'title': 'AutoCAD for Engineers', 'cat': 'ME', 'desc': 'Master AutoCAD for engineering design', 'hours': 40, 'fee': 2800.00, 'capacity': 25, 'level': 'Intermediate'},
        ]
        
        cat_map = {c.category_code: c for c in categories}
        
        for c in courses_data:
            course = Course(
                course_code=c['code'],
                course_title=c['title'],
                category_id=cat_map[c['cat']].category_id,
                description=c['desc'],
                duration_hours=c['hours'],
                fee_amount=c['fee'],
                fee_currency='ETB',
                max_capacity=c['capacity'],
                course_level=c['level'],
                certification_available=True,
                status='Active'
            )
            db.session.add(course)
        db.session.commit()
        courses = Course.query.all()
        print(f"✅ Inserted {len(courses)} courses")
        
        # 4. Insert Instructors
        print("👨‍🏫 Inserting instructors...")
        instructors_data = [
            {'code': 'INS-001', 'first': 'Dr. Abebe', 'last': 'Teshome', 'gender': 'Male', 
             'email': 'abebe.teshome@univ.edu', 'phone': '0911234567', 'qual': 'PhD Computer Science', 
             'exp': 18, 'dept': 'IT'},
            {'code': 'INS-002', 'first': 'Dr. Tigist', 'last': 'Wolde', 'gender': 'Female',
             'email': 'tigist.wolde@univ.edu', 'phone': '0922345678', 'qual': 'PhD Electrical Engineering',
             'exp': 15, 'dept': 'Electrical'},
            {'code': 'INS-003', 'first': 'Eng. Chalachew', 'last': 'Assefa', 'gender': 'Male',
             'email': 'chalachew.assefa@univ.edu', 'phone': '0933456789', 'qual': 'MSc Software Engineering',
             'exp': 12, 'dept': 'Software'},
            {'code': 'INS-004', 'first': 'Ms. Kidist', 'last': 'Tadesse', 'gender': 'Female',
             'email': 'kidist.tadesse@univ.edu', 'phone': '0944567890', 'qual': 'MBA Project Management',
             'exp': 10, 'dept': 'Business'},
        ]
        
        for i in instructors_data:
            instructor = Instructor(
                instructor_code=i['code'],
                first_name=i['first'],
                last_name=i['last'],
                gender=i['gender'],
                email=i['email'],
                phone_number=i['phone'],
                qualification=i['qual'],
                years_of_experience=i['exp'],
                department=i['dept'],
                employment_type='Full Time',
                joining_date=datetime(2015, 1, 1),
                status='Active'
            )
            db.session.add(instructor)
        db.session.commit()
        instructors = Instructor.query.all()
        print(f"✅ Inserted {len(instructors)} instructors")
        
        # 5. Insert Trainees
        print("👨‍🎓 Inserting trainees...")
        trainees_data = [
            {'code': 'T-001', 'first': 'Abebe', 'middle': 'Kebede', 'last': 'Tesfaye', 'dob': '1998-05-15', 'gender': 'Male',
             'email': 'abebe@email.com', 'phone': '0912345678', 'edu': 'BSc', 'emergency': 'Worku Tesfaye', 'emergency_phone': '0912345680'},
            {'code': 'T-002', 'first': 'Birtukan', 'middle': 'Hailu', 'last': 'Wolde', 'dob': '1999-08-22', 'gender': 'Female',
             'email': 'birtukan@email.com', 'phone': '0923456789', 'edu': 'BSc', 'emergency': 'Hailu Wolde', 'emergency_phone': '0923456790'},
            {'code': 'T-003', 'first': 'Chala', 'middle': 'Dereje', 'last': 'Hailu', 'dob': '1997-11-03', 'gender': 'Male',
             'email': 'chala@email.com', 'phone': '0934567890', 'edu': 'MSc', 'emergency': 'Dereje Hailu', 'emergency_phone': '0934567892'},
            {'code': 'T-004', 'first': 'Desta', 'middle': 'Alemayehu', 'last': 'Bekele', 'dob': '2000-03-10', 'gender': 'Male',
             'email': 'desta@email.com', 'phone': '0945678901', 'edu': 'High School', 'emergency': 'Alemayehu Bekele', 'emergency_phone': '0945678902'},
            {'code': 'T-005', 'first': 'Emebet', 'middle': 'Tesfaye', 'last': 'Girma', 'dob': '1996-07-25', 'gender': 'Female',
             'email': 'emebet@email.com', 'phone': '0956789012', 'edu': 'Diploma', 'emergency': 'Tesfaye Girma', 'emergency_phone': '0956789014'},
        ]
        
        for t in trainees_data:
            trainee = Trainee(
                trainee_code=t['code'],
                first_name=t['first'],
                middle_name=t['middle'],
                last_name=t['last'],
                date_of_birth=datetime.strptime(t['dob'], '%Y-%m-%d'),
                gender=t['gender'],
                email=t['email'],
                phone_number=t['phone'],
                educational_level=t['edu'],
                emergency_contact_name=t['emergency'],
                emergency_contact_phone=t['emergency_phone'],
                registration_date=datetime.now(),
                status='Active'
            )
            db.session.add(trainee)
        db.session.commit()
        trainees = Trainee.query.all()
        print(f"✅ Inserted {len(trainees)} trainees")
        
        # 6. Insert Batches
        print("📅 Inserting batches...")
        batches_data = [
            {'code': 'B-001', 'name': 'Python Batch 1', 'course': 'C101', 'start': '2024-02-01', 'end': '2024-03-28', 'capacity': 25},
            {'code': 'B-002', 'name': 'Python Batch 2', 'course': 'C101', 'start': '2024-03-01', 'end': '2024-04-25', 'capacity': 20},
            {'code': 'B-003', 'name': 'Electrical Safety Batch 1', 'course': 'C102', 'start': '2024-02-15', 'end': '2024-04-05', 'capacity': 25},
            {'code': 'B-004', 'name': 'PHP Batch 1', 'course': 'C103', 'start': '2024-03-01', 'end': '2024-05-10', 'capacity': 20},
            {'code': 'B-005', 'name': 'Project Management Batch 1', 'course': 'C104', 'start': '2024-02-20', 'end': '2024-04-12', 'capacity': 30},
            {'code': 'B-006', 'name': 'AutoCAD Batch 1', 'course': 'C106', 'start': '2024-02-10', 'end': '2024-04-04', 'capacity': 20},
        ]
        
        course_map = {c.course_code: c for c in courses}
        
        for b in batches_data:
            batch = Batch(
                batch_code=b['code'],
                batch_name=b['name'],
                course_id=course_map[b['course']].course_id,
                start_date=datetime.strptime(b['start'], '%Y-%m-%d'),
                end_date=datetime.strptime(b['end'], '%Y-%m-%d'),
                schedule_type='Weekday',
                max_capacity=b['capacity'],
                min_trainees_required=5,
                status='Ongoing' if b['code'] in ['B-001', 'B-003', 'B-005', 'B-006'] else 'Upcoming'
            )
            db.session.add(batch)
        db.session.commit()
        batches = Batch.query.all()
        print(f"✅ Inserted {len(batches)} batches")
        
        # 7. Insert Enrollments
        print("📝 Inserting enrollments...")
        # Map trainees and batches
        trainee_map = {t.trainee_code: t for t in trainees}
        batch_map = {b.batch_code: b for b in batches}
        
        enrollments_data = [
            {'trainee': 'T-001', 'batch': 'B-001'},
            {'trainee': 'T-002', 'batch': 'B-001'},
            {'trainee': 'T-003', 'batch': 'B-001'},
            {'trainee': 'T-004', 'batch': 'B-001'},
            {'trainee': 'T-005', 'batch': 'B-003'},
            {'trainee': 'T-001', 'batch': 'B-005'},
            {'trainee': 'T-002', 'batch': 'B-006'},
        ]
        
        for idx, e in enumerate(enrollments_data, 1):
            enrollment = Enrollment(
                enrollment_number=f'E-{idx:03d}',
                trainee_id=trainee_map[e['trainee']].trainee_id,
                batch_id=batch_map[e['batch']].batch_id,
                enrollment_date=datetime.now() - timedelta(days=random.randint(5, 30)),
                status='Active',
                payment_status=random.choice(['Paid', 'Pending'])
            )
            db.session.add(enrollment)
        db.session.commit()
        enrollments = Enrollment.query.all()
        print(f"✅ Inserted {len(enrollments)} enrollments")
        
        # 8. Insert Class Sessions
        print("📖 Inserting class sessions...")
        instructor_map = {i.instructor_code: i for i in instructors}
        sessions_data = [
            {'batch': 'B-001', 'date': '2024-02-01', 'topic': 'Introduction to Python', 'instructor': 'INS-001'},
            {'batch': 'B-001', 'date': '2024-02-03', 'topic': 'Python Syntax', 'instructor': 'INS-001'},
            {'batch': 'B-001', 'date': '2024-02-05', 'topic': 'Control Structures', 'instructor': 'INS-001'},
            {'batch': 'B-003', 'date': '2024-02-17', 'topic': 'Electrical Safety Intro', 'instructor': 'INS-002'},
            {'batch': 'B-005', 'date': '2024-02-25', 'topic': 'Project Management Intro', 'instructor': 'INS-004'},
            {'batch': 'B-006', 'date': '2024-02-12', 'topic': 'AutoCAD Basics', 'instructor': 'INS-003'},
        ]
        
        for idx, s in enumerate(sessions_data, 1):
            session = ClassSession(
                session_code=f'S-{idx:03d}',
                batch_id=batch_map[s['batch']].batch_id,
                session_date=datetime.strptime(s['date'], '%Y-%m-%d'),
                start_time=datetime.strptime('09:00:00', '%H:%M:%S').time(),
                end_time=datetime.strptime('12:00:00', '%H:%M:%S').time(),
                topic_covered=s['topic'],
                session_type='Lecture',
                instructor_id=instructor_map[s['instructor']].instructor_id,
                room_number=f'Room {100 + idx}',
                status='Completed'
            )
            db.session.add(session)
        db.session.commit()
        sessions = ClassSession.query.all()
        print(f"✅ Inserted {len(sessions)} class sessions")
        
        # 9. Insert Attendance Records
        print("📋 Inserting attendance records...")
        statuses = ['Present', 'Present', 'Present', 'Late', 'Absent']
        
        for session in sessions[:4]:  # First 4 sessions
            # Get enrollments for this batch
            batch_enrollments = [e for e in enrollments if e.batch_id == session.batch_id]
            for enrollment in batch_enrollments[:5]:  # First 5 trainees
                status = random.choice(statuses)
                attendance = AttendanceRecord(
                    session_id=session.session_id,
                    trainee_id=enrollment.trainee_id,
                    status=status,
                    check_in_time=datetime.strptime('09:00:00', '%H:%M:%S').time() if status == 'Present' else None,
                    check_out_time=datetime.strptime('12:00:00', '%H:%M:%S').time() if status == 'Present' else None,
                    remarks='' if status == 'Present' else 'Excused' if status == 'Absent' else 'Traffic',
                    recorded_by=1  # Admin user ID
                )
                db.session.add(attendance)
        db.session.commit()
        print(f"✅ Inserted attendance records")
        
        # 10. Insert Assessments
        print("📝 Inserting assessments...")
        assessments_data = [
            {'code': 'A-001', 'batch': 'B-001', 'title': 'Quiz 1 - Python Basics', 'type': 'Quiz', 'max_marks': 20, 'weight': 20, 'passing': 10},
            {'code': 'A-002', 'batch': 'B-001', 'title': 'Midterm - Python', 'type': 'Exam', 'max_marks': 50, 'weight': 30, 'passing': 25},
            {'code': 'A-003', 'batch': 'B-003', 'title': 'Quiz - Safety Standards', 'type': 'Quiz', 'max_marks': 20, 'weight': 20, 'passing': 10},
        ]
        
        for a in assessments_data:
            assessment = Assessment(
                assessment_code=a['code'],
                batch_id=batch_map[a['batch']].batch_id,
                title=a['title'],
                assessment_type=a['type'],
                max_marks=a['max_marks'],
                weightage_percent=a['weight'],
                passing_marks=a['passing'],
                assessment_date=datetime.now() - timedelta(days=random.randint(1, 10)),
                status='Completed'
            )
            db.session.add(assessment)
        db.session.commit()
        assessments = Assessment.query.all()
        print(f"✅ Inserted {len(assessments)} assessments")
        
        # 11. Insert Trainee Results
        print("📊 Inserting trainee results...")
        grade_map = {g.grade_letter: g for g in GradeScale.query.all()}
        
        for assessment in assessments:
            # Get enrollments for this batch
            batch_enrollments = [e for e in enrollments if e.batch_id == assessment.batch_id]
            for enrollment in batch_enrollments[:4]:  # First 4 trainees
                marks = random.randint(10, assessment.max_marks)
                percentage = (marks / assessment.max_marks) * 100
                
                # Determine grade
                grade_letter = 'F'
                for g in GradeScale.query.order_by(GradeScale.min_percentage.desc()).all():
                    if percentage >= g.min_percentage:
                        grade_letter = g.grade_letter
                        break
                
                result = TraineeResult(
                    assessment_id=assessment.assessment_id,
                    trainee_id=enrollment.trainee_id,
                    marks_obtained=marks,
                    percentage_score=percentage,
                    grade=grade_letter,
                    status='Pass' if percentage >= 50 else 'Fail',
                    comments=f'Score: {marks}/{assessment.max_marks}',
                    is_verified=True
                )
                db.session.add(result)
        db.session.commit()
        print(f"✅ Inserted trainee results")
        
        # 12. Insert Users (if they don't exist)
        print("👤 Inserting users...")
        existing_users = User.query.all()
        if not existing_users:
            users_data = [
                {'username': 'admin', 'email': 'admin@sttims.com', 'role': 'Admin'},
                {'username': 'manager', 'email': 'manager@sttims.com', 'role': 'Manager'},
                {'username': 'instructor1', 'email': 'abebe.teshome@univ.edu', 'role': 'Instructor', 'instructor_id': 1},
                {'username': 'trainee1', 'email': 'abebe@email.com', 'role': 'Trainee', 'trainee_id': 1},
            ]
            
            for u in users_data:
                user = User(
                    username=u['username'],
                    email=u['email'],
                    role=u['role'],
                    trainee_id=u.get('trainee_id'),
                    instructor_id=u.get('instructor_id'),
                    status='Active'
                )
                user.set_password('Password123!')
                db.session.add(user)
            db.session.commit()
        print(f"✅ Users ready")
        
        # Final summary
        print("\n" + "="*50)
        print("✅ SAMPLE DATA INSERTION COMPLETE!")
        print("="*50)
        print(f"📊 Grade Scale: {GradeScale.query.count()}")
        print(f"📂 Categories: {Category.query.count()}")
        print(f"📚 Courses: {Course.query.count()}")
        print(f"👨‍🏫 Instructors: {Instructor.query.count()}")
        print(f"👨‍🎓 Trainees: {Trainee.query.count()}")
        print(f"📅 Batches: {Batch.query.count()}")
        print(f"📝 Enrollments: {Enrollment.query.count()}")
        print(f"📖 Sessions: {ClassSession.query.count()}")
        print(f"📋 Attendance: {AttendanceRecord.query.count()}")
        print(f"📝 Assessments: {Assessment.query.count()}")
        print(f"📊 Results: {TraineeResult.query.count()}")
        print(f"👤 Users: {User.query.count()}")
        print("="*50)
        
        print("\n🔑 Default Passwords:")
        print("  - admin / Password123!")
        print("  - manager / Password123!")
        print("  - instructor1 / Password123!")
        print("  - trainee1 / Password123!")

if __name__ == "__main__":
    insert_sample_data()
