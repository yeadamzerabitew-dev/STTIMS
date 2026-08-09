#!/usr/bin/env python
"""Add sample data to STTIMS database"""

from app import app
from models import db, User, Trainee, Instructor, Course, Category, Batch, Enrollment, Certificate
from datetime import datetime, timedelta
import random

def add_data():
    with app.app_context():
        print("📊 Adding sample data...")
        
        # Check if data exists
        if Trainee.query.count() > 0:
            print("⚠️ Data already exists. Skipping...")
            return
        
        # Create Categories
        print("Creating categories...")
        categories = []
        for name, code in [('IT', 'IT'), ('Business', 'BUS'), ('Data Science', 'DS')]:
            cat = Category(category_name=name, category_code=code, status='Active')
            db.session.add(cat)
            categories.append(cat)
        db.session.commit()
        print(f"✅ Created {len(categories)} categories")
        
        # Create Courses
        print("Creating courses...")
        courses = []
        course_data = [
            ('PY101', 'Python Programming', 'IT', 40, 1500),
            ('JS101', 'JavaScript', 'IT', 35, 1200),
            ('SQL101', 'SQL Database', 'IT', 30, 1000),
            ('DS101', 'Data Science Intro', 'DS', 45, 2000),
            ('BUS101', 'Business Management', 'BUS', 30, 800),
        ]
        
        for code, title, cat_code, hours, fee in course_data:
            cat = Category.query.filter_by(category_code=cat_code).first()
            course = Course(
                course_code=code,
                course_title=title,
                category_id=cat.category_id,
                description=f'Learn {title}',
                duration_hours=hours,
                fee_amount=fee,
                max_capacity=20,
                status='Active'
            )
            db.session.add(course)
            courses.append(course)
        db.session.commit()
        print(f"✅ Created {len(courses)} courses")
        
        # Create Trainees
        print("Creating trainees...")
        trainees = []
        trainee_data = [
            ('T001', 'John', 'Doe', 'john@email.com', '0912345678', 'Male', 'BSc'),
            ('T002', 'Jane', 'Smith', 'jane@email.com', '0912345679', 'Female', 'MSc'),
            ('T003', 'Bob', 'Johnson', 'bob@email.com', '0912345680', 'Male', 'Diploma'),
        ]
        
        for code, first, last, email, phone, gender, edu in trainee_data:
            trainee = Trainee(
                trainee_code=code,
                first_name=first,
                last_name=last,
                email=email,
                phone_number=phone,
                gender=gender,
                date_of_birth=datetime(1990, 1, 1),
                educational_level=edu,
                emergency_contact_name=f'{first} {last} Sr.',
                emergency_contact_phone=f'09{random.randint(10000000, 99999999)}',
                status='Active'
            )
            db.session.add(trainee)
            trainees.append(trainee)
        db.session.commit()
        print(f"✅ Created {len(trainees)} trainees")
        
        # Create Instructors
        print("Creating instructors...")
        instructor_data = [
            ('INS001', 'Dr. Sarah', 'Smith', 'sarah@email.com', '0912345690', 'Female', 'PhD CS', 10, 'IT'),
            ('INS002', 'Prof. James', 'Wilson', 'james@email.com', '0912345691', 'Male', 'PhD DS', 12, 'DS'),
        ]
        
        for code, first, last, email, phone, gender, qual, exp, dept in instructor_data:
            instructor = Instructor(
                instructor_code=code,
                first_name=first,
                last_name=last,
                email=email,
                phone_number=phone,
                gender=gender,
                date_of_birth=datetime(1980, 1, 1),
                qualification=qual,
                years_of_experience=exp,
                employment_type='Full Time',
                joining_date=datetime(2015, 1, 1),
                department=dept,
                status='Active'
            )
            db.session.add(instructor)
        db.session.commit()
        print(f"✅ Created instructors")
        
        # Create Batches
        print("Creating batches...")
        batches = []
        for i, course in enumerate(courses):
            start_date = datetime.now().date() + timedelta(days=random.randint(1, 15))
            batch = Batch(
                batch_code=f'B00{i+1}',
                batch_name=f'Batch {i+1} - {course.course_title}',
                course_id=course.course_id,
                start_date=start_date,
                end_date=start_date + timedelta(days=30),
                schedule_type='Weekday',
                max_capacity=15 + random.randint(0, 10),
                status='Upcoming'
            )
            db.session.add(batch)
            batches.append(batch)
        db.session.commit()
        print(f"✅ Created {len(batches)} batches")
        
        # Create Enrollments
        print("Creating enrollments...")
        for trainee in trainees:
            for batch in batches[:2]:
                enrollment = Enrollment(
                    trainee_id=trainee.trainee_id,
                    batch_id=batch.batch_id,
                    enrollment_date=datetime.now(),
                    status='Active',
                    payment_status='Paid'
                )
                db.session.add(enrollment)
        db.session.commit()
        print("✅ Created enrollments")
        
        print("=" * 50)
        print("✅ Sample data added successfully!")
        print("=" * 50)
        print(f"Categories: {Category.query.count()}")
        print(f"Courses: {Course.query.count()}")
        print(f"Trainees: {Trainee.query.count()}")
        print(f"Instructors: {Instructor.query.count()}")
        print(f"Batches: {Batch.query.count()}")
        print(f"Enrollments: {Enrollment.query.count()}")
        print("=" * 50)

if __name__ == '__main__':
    add_data()
