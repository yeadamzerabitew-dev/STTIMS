#!/usr/bin/env python
"""Minimal data seeding for STTIMS"""

from app import app
from models import db, User, Trainee, Instructor, Course, Category, Batch, Enrollment
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def seed_minimal():
    with app.app_context():
        print("=" * 60)
        print("📊 STTIMS - Minimal Data Seeding")
        print("=" * 60)
        
        # Check if users exist
        if User.query.count() > 0:
            print("⚠️ Users already exist! Skipping...")
            return
        
        print("📁 Creating minimal data...")
        
        # =============================================
        # 1. Create Categories
        # =============================================
        print("📁 Creating categories...")
        cat1 = Category(
            category_name='Information Technology',
            category_code='IT',
            description='IT Courses',
            status='Active'
        )
        db.session.add(cat1)
        
        cat2 = Category(
            category_name='Business',
            category_code='BUS',
            description='Business Courses',
            status='Active'
        )
        db.session.add(cat2)
        db.session.commit()
        print("✅ Categories created")

        # =============================================
        # 2. Create Courses
        # =============================================
        print("📚 Creating courses...")
        course1 = Course(
            course_code='PY101',
            course_title='Python Programming',
            category_id=cat1.category_id,
            description='Learn Python programming',
            duration_hours=40,
            fee_amount=1500,
            max_capacity=20,
            status='Active'
        )
        db.session.add(course1)
        
        course2 = Course(
            course_code='BUS101',
            course_title='Business Management',
            category_id=cat2.category_id,
            description='Learn business management',
            duration_hours=30,
            fee_amount=800,
            max_capacity=30,
            status='Active'
        )
        db.session.add(course2)
        db.session.commit()
        print("✅ Courses created")

        # =============================================
        # 3. Create Trainees
        # =============================================
        print("👨‍🎓 Creating trainees...")
        trainee1 = Trainee(
            trainee_code='T001',
            first_name='John',
            last_name='Doe',
            email='john@email.com',
            phone_number='0912345678',
            gender='Male',
            date_of_birth=datetime(1990, 1, 1),
            educational_level='BSc',
            emergency_contact_name='Jane Doe',
            emergency_contact_phone='0912345679',
            status='Active'
        )
        db.session.add(trainee1)
        
        trainee2 = Trainee(
            trainee_code='T002',
            first_name='Jane',
            last_name='Smith',
            email='jane@email.com',
            phone_number='0912345680',
            gender='Female',
            date_of_birth=datetime(1992, 2, 1),
            educational_level='MSc',
            emergency_contact_name='John Smith',
            emergency_contact_phone='0912345681',
            status='Active'
        )
        db.session.add(trainee2)
        db.session.commit()
        print("✅ Trainees created")

        # =============================================
        # 4. Create Instructors
        # =============================================
        print("👨‍🏫 Creating instructors...")
        instructor1 = Instructor(
            instructor_code='INS001',
            first_name='Dr. Sarah',
            last_name='Smith',
            email='sarah@sttims.com',
            phone_number='0912345690',
            gender='Female',
            date_of_birth=datetime(1980, 1, 1),
            qualification='PhD Computer Science',
            years_of_experience=10,
            employment_type='Full Time',
            joining_date=datetime(2015, 1, 1),
            department='IT',
            status='Active'
        )
        db.session.add(instructor1)
        db.session.commit()
        print("✅ Instructors created")

        # =============================================
        # 5. Create Batches
        # =============================================
        print("📦 Creating batches...")
        batch1 = Batch(
            batch_code='B001',
            batch_name='Python Batch 1',
            course_id=course1.course_id,
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=30),
            schedule_type='Weekday',
            max_capacity=20,
            current_enrollment=5,
            status='Ongoing'
        )
        db.session.add(batch1)
        
        batch2 = Batch(
            batch_code='B002',
            batch_name='Business Batch 1',
            course_id=course2.course_id,
            start_date=datetime.now().date() + timedelta(days=10),
            end_date=datetime.now().date() + timedelta(days=40),
            schedule_type='Weekend',
            max_capacity=30,
            current_enrollment=8,
            status='Upcoming'
        )
        db.session.add(batch2)
        db.session.commit()
        print("✅ Batches created")

        # =============================================
        # 6. Create Enrollments
        # =============================================
        print("📝 Creating enrollments...")
        enrollment1 = Enrollment(
            trainee_id=trainee1.trainee_id,
            batch_id=batch1.batch_id,
            enrollment_date=datetime.now(),
            status='Active',
            payment_status='Paid'
        )
        db.session.add(enrollment1)
        
        enrollment2 = Enrollment(
            trainee_id=trainee2.trainee_id,
            batch_id=batch1.batch_id,
            enrollment_date=datetime.now(),
            status='Active',
            payment_status='Pending'
        )
        db.session.add(enrollment2)
        db.session.commit()
        print("✅ Enrollments created")

        # =============================================
        # 7. Create Users
        # =============================================
        print("👤 Creating users...")
        
        # Link trainee to user
        admin = User(
            username='admin',
            email='admin@sttims.com',
            role='Admin',
            status='Active'
        )
        admin.set_password('Admin123!')
        db.session.add(admin)
        
        manager = User(
            username='manager',
            email='manager@sttims.com',
            role='Manager',
            status='Active'
        )
        manager.set_password('Manager123!')
        db.session.add(manager)
        
        instructor_user = User(
            username='instructor',
            email='instructor@sttims.com',
            role='Instructor',
            status='Active',
            instructor_id=instructor1.instructor_id
        )
        instructor_user.set_password('Instructor123!')
        db.session.add(instructor_user)
        
        trainee_user = User(
            username='trainee',
            email='trainee@sttims.com',
            role='Trainee',
            status='Active',
            trainee_id=trainee1.trainee_id
        )
        trainee_user.set_password('Trainee123!')
        db.session.add(trainee_user)
        db.session.commit()
        print("✅ Users created")

        # =============================================
        # Summary
        # =============================================
        print("\n" + "=" * 60)
        print("✅ Minimal data seeded successfully!")
        print("=" * 60)
        print("📊 Data Summary:")
        print(f"  Users: {User.query.count()}")
        print(f"  Categories: {Category.query.count()}")
        print(f"  Courses: {Course.query.count()}")
        print(f"  Trainees: {Trainee.query.count()}")
        print(f"  Instructors: {Instructor.query.count()}")
        print(f"  Batches: {Batch.query.count()}")
        print(f"  Enrollments: {Enrollment.query.count()}")
        print("=" * 60)
        print("🔑 Test Credentials:")
        print("  Admin:      admin / Admin123!")
        print("  Manager:    manager / Manager123!")
        print("  Instructor: instructor / Instructor123!")
        print("  Trainee:    trainee / Trainee123!")
        print("=" * 60)

if __name__ == '__main__':
    seed_minimal()
