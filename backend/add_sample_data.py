#!/usr/bin/env python
"""Add sample data to STTIMS database"""

from app import app
from models import db, User, Trainee, Instructor, Course, Category, Batch, Enrollment, Certificate
from datetime import datetime, timedelta
import random

def add_sample_data():
    with app.app_context():
        print("📊 Adding sample data to STTIMS...")
        
        # Check if data already exists
        if Trainee.query.count() > 0:
            print("⚠️ Data already exists. Skipping...")
            return
        
        # =============================================
        # 1. Create Categories
        # =============================================
        print("📁 Creating categories...")
        categories = [
            Category(category_name='Information Technology', category_code='IT', status='Active'),
            Category(category_name='Business Management', category_code='BUS', status='Active'),
            Category(category_name='Data Science', category_code='DS', status='Active'),
            Category(category_name='Software Engineering', category_code='SE', status='Active'),
            Category(category_name='Networking', category_code='NET', status='Active'),
        ]
        for cat in categories:
            db.session.add(cat)
        db.session.commit()
        print(f"✅ Created {len(categories)} categories")

        # =============================================
        # 2. Create Courses
        # =============================================
        print("📚 Creating courses...")
        courses_data = [
            {'code': 'PY101', 'title': 'Python Programming', 'cat': 'IT', 'desc': 'Learn Python from scratch', 'hours': 40, 'fee': 1500, 'capacity': 20},
            {'code': 'JS101', 'title': 'JavaScript Fundamentals', 'cat': 'IT', 'desc': 'Master JavaScript for web development', 'hours': 35, 'fee': 1200, 'capacity': 25},
            {'code': 'SQL101', 'title': 'SQL Database Design', 'cat': 'IT', 'desc': 'Learn SQL and database design', 'hours': 30, 'fee': 1000, 'capacity': 20},
            {'code': 'DS101', 'title': 'Data Science Introduction', 'cat': 'DS', 'desc': 'Introduction to data science', 'hours': 45, 'fee': 2000, 'capacity': 15},
            {'code': 'ML101', 'title': 'Machine Learning Basics', 'cat': 'DS', 'desc': 'Learn machine learning fundamentals', 'hours': 50, 'fee': 2500, 'capacity': 15},
            {'code': 'BUS101', 'title': 'Business Management', 'cat': 'BUS', 'desc': 'Principles of business management', 'hours': 30, 'fee': 800, 'capacity': 30},
            {'code': 'SE101', 'title': 'Software Engineering', 'cat': 'SE', 'desc': 'Software development lifecycle', 'hours': 40, 'fee': 1800, 'capacity': 20},
            {'code': 'NET101', 'title': 'Network Fundamentals', 'cat': 'NET', 'desc': 'Computer networking basics', 'hours': 35, 'fee': 1200, 'capacity': 20},
        ]
        
        courses = []
        for c in courses_data:
            category = Category.query.filter_by(category_code=c['cat']).first()
            course = Course(
                course_code=c['code'],
                course_title=c['title'],
                category_id=category.category_id if category else None,
                description=c['desc'],
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
            {'code': 'T001', 'first': 'John', 'last': 'Doe', 'email': 'john@example.com', 'phone': '0912345678', 'gender': 'Male', 'edu': 'BSc'},
            {'code': 'T002', 'first': 'Jane', 'last': 'Smith', 'email': 'jane@example.com', 'phone': '0912345679', 'gender': 'Female', 'edu': 'MSc'},
            {'code': 'T003', 'first': 'Bob', 'last': 'Johnson', 'email': 'bob@example.com', 'phone': '0912345680', 'gender': 'Male', 'edu': 'Diploma'},
            {'code': 'T004', 'first': 'Alice', 'last': 'Williams', 'email': 'alice@example.com', 'phone': '0912345681', 'gender': 'Female', 'edu': 'BSc'},
            {'code': 'T005', 'first': 'Charlie', 'last': 'Brown', 'email': 'charlie@example.com', 'phone': '0912345682', 'gender': 'Male', 'edu': 'High School'},
            {'code': 'T006', 'first': 'Diana', 'last': 'Jones', 'email': 'diana@example.com', 'phone': '0912345683', 'gender': 'Female', 'edu': 'MSc'},
            {'code': 'T007', 'first': 'Eve', 'last': 'Davis', 'email': 'eve@example.com', 'phone': '0912345684', 'gender': 'Female', 'edu': 'BSc'},
            {'code': 'T008', 'first': 'Frank', 'last': 'Miller', 'email': 'frank@example.com', 'phone': '0912345685', 'gender': 'Male', 'edu': 'Diploma'},
        ]
        
        trainees = []
        for t in trainees_data:
            trainee = Trainee(
                trainee_code=t['code'],
                first_name=t['first'],
                last_name=t['last'],
                email=t['email'],
                phone_number=t['phone'],
                gender=t['gender'],
                date_of_birth=datetime(1990 + random.randint(0, 10), random.randint(1, 12), random.randint(1, 28)),
                educational_level=t['edu'],
                emergency_contact_name=f"{t['first']} {t['last']} Sr.",
                emergency_contact_phone=f"09{random.randint(10000000, 99999999)}",
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
            {'code': 'INS001', 'first': 'Dr. Sarah', 'last': 'Smith', 'email': 'sarah@example.com', 'phone': '0912345690', 'gender': 'Female', 'qual': 'PhD Computer Science', 'exp': 10, 'dept': 'IT'},
            {'code': 'INS002', 'first': 'Prof. James', 'last': 'Wilson', 'email': 'james@example.com', 'phone': '0912345691', 'gender': 'Male', 'qual': 'PhD Data Science', 'exp': 12, 'dept': 'DS'},
            {'code': 'INS003', 'first': 'Dr. Maria', 'last': 'Garcia', 'email': 'maria@example.com', 'phone': '0912345692', 'gender': 'Female', 'qual': 'MBA Business', 'exp': 8, 'dept': 'BUS'},
            {'code': 'INS004', 'first': 'Prof. Robert', 'last': 'Taylor', 'email': 'robert@example.com', 'phone': '0912345693', 'gender': 'Male', 'qual': 'MS Software Engineering', 'exp': 15, 'dept': 'SE'},
        ]
        
        for i in instructors_data:
            instructor = Instructor(
                instructor_code=i['code'],
                first_name=i['first'],
                last_name=i['last'],
                email=i['email'],
                phone_number=i['phone'],
                gender=i['gender'],
                date_of_birth=datetime(1970 + random.randint(0, 15), random.randint(1, 12), random.randint(1, 28)),
                qualification=i['qual'],
                years_of_experience=i['exp'],
                employment_type='Full Time',
                joining_date=datetime(2015 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
                department=i['dept'],
                status='Active'
            )
            db.session.add(instructor)
        db.session.commit()
        print(f"✅ Created {len(instructors_data)} instructors")

        # =============================================
        # 5. Create Batches
        # =============================================
        print("📦 Creating batches...")
        batch_names = ['Morning', 'Evening', 'Weekend', 'Intensive']
        schedule_types = ['Weekday', 'Evening', 'Weekend', 'Intensive']
        
        batches = []
        for i, course in enumerate(courses[:6]):  # Only use first 6 courses
            instructor = Instructor.query.offset(i % len(instructors_data)).first()
            for j in range(2):  # 2 batches per course
                start_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
                batch = Batch(
                    batch_code=f"B{str(i+1).zfill(2)}{str(j+1).zfill(2)}",
                    batch_name=f"{course.course_title} - {batch_names[j % len(batch_names)]}",
                    course_id=course.course_id,
                    start_date=start_date,
                    end_date=start_date + timedelta(days=30 + random.randint(0, 15)),
                    schedule_type=schedule_types[j % len(schedule_types)],
                    max_capacity=15 + random.randint(0, 15),
                    status=random.choice(['Upcoming', 'Ongoing', 'Completed']),
                    instructor_id=instructor.instructor_id if instructor else None
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
            # Each trainee enrolls in 1-3 courses
            num_courses = random.randint(1, 3)
            selected_batches = random.sample(batches, min(num_courses, len(batches)))
            
            for batch in selected_batches:
                status = random.choices(['Active', 'Completed', 'Dropped'], weights=[70, 20, 10])[0]
                payment_status = random.choices(['Paid', 'Pending', 'Partial'], weights=[60, 25, 15])[0]
                
                enrollment = Enrollment(
                    trainee_id=trainee.trainee_id,
                    batch_id=batch.batch_id,
                    enrollment_date=datetime.now() - timedelta(days=random.randint(0, 60)),
                    status=status,
                    payment_status=payment_status
                )
                db.session.add(enrollment)
                enrollments.append(enrollment)
        db.session.commit()
        print(f"✅ Created {len(enrollments)} enrollments")

        # =============================================
        # 7. Create Certificates
        # =============================================
        print("🎓 Creating certificates...")
        completed_enrollments = Enrollment.query.filter_by(status='Completed').all()
        
        for enrollment in completed_enrollments[:10]:  # Only create for first 10 completed
            certificate = Certificate(
                enrollment_id=enrollment.enrollment_id,
                certificate_number=f"CERT-{datetime.now().year()}-{str(enrollment.enrollment_id).zfill(5)}",
                issue_date=datetime.now(),
                status='Issued',
                verification_token=f"VERIFY-{datetime.now().year()}-{random.randint(10000, 99999)}"
            )
            db.session.add(certificate)
        db.session.commit()
        print(f"✅ Created certificates for {len(completed_enrollments[:10])} completed enrollments")

        print("\n" + "=" * 50)
        print("✅ Sample data added successfully!")
        print("=" * 50)
        print(f"📊 Summary:")
        print(f"   - Categories: {Category.query.count()}")
        print(f"   - Courses: {Course.query.count()}")
        print(f"   - Trainees: {Trainee.query.count()}")
        print(f"   - Instructors: {Instructor.query.count()}")
        print(f"   - Batches: {Batch.query.count()}")
        print(f"   - Enrollments: {Enrollment.query.count()}")
        print(f"   - Certificates: {Certificate.query.count()}")
        print("=" * 50)

if __name__ == '__main__':
    add_sample_data()
