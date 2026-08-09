#!/usr/bin/env python
"""Add sample data to STTIMS database - Fixed Version"""

from app import app
from models import db, Trainee, Instructor, Course, Category, Batch, Enrollment
from datetime import datetime, timedelta
import random

def add_data():
    with app.app_context():
        print("📊 Adding sample data to STTIMS...")
        
        # Check if batches already exist
        if Batch.query.count() > 0:
            print("⚠️ Batches already exist. Skipping...")
            return
        
        print(f"📁 Found {Category.query.count()} categories")
        print(f"📚 Found {Course.query.count()} courses")
        print(f"👨‍🎓 Found {Trainee.query.count()} trainees")
        print(f"👨‍🏫 Found {Instructor.query.count()} instructors")
        
        # =============================================
        # 1. Create Batches (Simplified)
        # =============================================
        print("📦 Creating batches...")
        courses = Course.query.all()
        instructors = Instructor.query.all()
        
        if not courses:
            print("❌ No courses found! Please add courses first.")
            return
        
        batches = []
        batch_names = ['Morning Batch', 'Evening Batch', 'Weekend Batch']
        schedule_types = ['Weekday', 'Evening', 'Weekend']
        
        for i, course in enumerate(courses[:6]):
            instructor = instructors[i % len(instructors)] if instructors else None
            
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
                    status=random.choice(['Upcoming', 'Ongoing', 'Completed'])
                )
                db.session.add(batch)
                batches.append(batch)
                print(f"  ✅ Created batch: {batch.batch_name}")
        
        db.session.commit()
        print(f"✅ Created {len(batches)} batches")

        # =============================================
        # 2. Create Enrollments
        # =============================================
        print("📝 Creating enrollments...")
        trainees = Trainee.query.all()
        enrollments = []
        
        for trainee in trainees:
            # Each trainee enrolls in 1-2 batches
            num_batches = random.randint(1, min(2, len(batches)))
            selected_batches = random.sample(batches, num_batches)
            
            for batch in selected_batches:
                status = random.choices(['Active', 'Completed'], weights=[70, 30])[0]
                payment_status = random.choices(['Paid', 'Pending'], weights=[70, 30])[0]
                
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
        # Summary
        # =============================================
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
        print("=" * 50)

if __name__ == '__main__':
    add_data()
