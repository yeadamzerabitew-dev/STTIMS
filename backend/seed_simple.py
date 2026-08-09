#!/usr/bin/env python
"""Simple data seeding for STTIMS"""

from app import app
from models import db, User, Trainee, Instructor, Course, Category, Batch, Enrollment
from datetime import datetime, timedelta
import random

def seed():
    with app.app_context():
        print("📊 Starting simple data seeding...")
        
        # Check if data exists
        if User.query.count() > 0:
            print("⚠️ Data already exists!")
            return
        
        print("👤 Creating users...")
        users = [
            User(username='admin', email='admin@sttims.com', role='Admin', status='Active'),
            User(username='manager', email='manager@sttims.com', role='Manager', status='Active'),
            User(username='instructor', email='instructor@sttims.com', role='Instructor', status='Active'),
            User(username='trainee', email='trainee@sttims.com', role='Trainee', status='Active'),
        ]
        for u in users:
            u.set_password('Password123!')
            db.session.add(u)
        db.session.commit()
        
        print("📁 Creating categories...")
        cats = []
        for name, code in [('IT', 'IT'), ('Business', 'BUS'), ('Data Science', 'DS')]:
            cat = Category(category_name=name, category_code=code, status='Active')
            db.session.add(cat)
            cats.append(cat)
        db.session.commit()
        
        print("📚 Creating courses...")
        courses = []
        for code, title, cat_code in [('PY101', 'Python', 'IT'), ('JS101', 'JavaScript', 'IT'), ('DS101', 'Data Science', 'DS')]:
            cat = next(c for c in cats if c.category_code == cat_code)
            course = Course(
                course_code=code,
                course_title=title,
                category_id=cat.category_id,
                description=f'Learn {title}',
                duration_hours=30,
                fee_amount=1000,
                max_capacity=20,
                status='Active'
            )
            db.session.add(course)
            courses.append(course)
        db.session.commit()
        
        print("👨‍🎓 Creating trainees...")
        for i in range(10):
            trainee = Trainee(
                trainee_code=f'T{str(i+1).zfill(3)}',
                first_name=f'Student{i+1}',
                last_name=f'Last{i+1}',
                email=f'student{i+1}@email.com',
                phone_number=f'09123456{str(i).zfill(2)}',
                gender=random.choice(['Male', 'Female']),
                date_of_birth=datetime(1990 + random.randint(0, 10), 1, 1),
                educational_level='BSc',
                emergency_contact_name='Emergency Contact',
                emergency_contact_phone='0912345699',
                status='Active'
            )
            db.session.add(trainee)
        db.session.commit()
        
        print("👨‍🏫 Creating instructors...")
        for i in range(3):
            instructor = Instructor(
                instructor_code=f'INS{str(i+1).zfill(3)}',
                first_name=f'Prof{i+1}',
                last_name=f'Last{i+1}',
                email=f'prof{i+1}@sttims.com',
                phone_number=f'09123457{str(i).zfill(2)}',
                gender=random.choice(['Male', 'Female']),
                date_of_birth=datetime(1970 + i, 1, 1),
                qualification='PhD',
                years_of_experience=10 + i,
                employment_type='Full Time',
                joining_date=datetime(2010 + i, 1, 1),
                department='IT',
                status='Active'
            )
            db.session.add(instructor)
        db.session.commit()
        
        print("📦 Creating batches...")
        for i, course in enumerate(courses[:3]):
            for j in range(2):
                batch = Batch(
                    batch_code=f'B{str(i+1).zfill(2)}{str(j+1).zfill(2)}',
                    batch_name=f'Batch {j+1} - {course.course_title}',
                    course_id=course.course_id,
                    start_date=datetime.now().date(),
                    end_date=datetime.now().date() + timedelta(days=30),
                    schedule_type='Weekday',
                    max_capacity=20,
                    current_enrollment=random.randint(5, 15),
                    status=random.choice(['Upcoming', 'Ongoing'])
                )
                db.session.add(batch)
        db.session.commit()
        
        print("📝 Creating enrollments...")
        trainees = Trainee.query.all()
        batches = Batch.query.all()
        for trainee in trainees[:8]:
            for batch in batches[:4]:
                enrollment = Enrollment(
                    trainee_id=trainee.trainee_id,
                    batch_id=batch.batch_id,
                    enrollment_date=datetime.now(),
                    status='Active',
                    payment_status='Paid'
                )
                db.session.add(enrollment)
        db.session.commit()
        
        print("✅ Data seeded successfully!")
        print(f"Users: {User.query.count()}")
        print(f"Categories: {Category.query.count()}")
        print(f"Courses: {Course.query.count()}")
        print(f"Trainees: {Trainee.query.count()}")
        print(f"Instructors: {Instructor.query.count()}")
        print(f"Batches: {Batch.query.count()}")
        print(f"Enrollments: {Enrollment.query.count()}")

if __name__ == '__main__':
    seed()
