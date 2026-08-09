from app import app
from models import db, User, Trainee, Instructor, Course, Category, Batch, Enrollment

with app.app_context():
    print("\n" + "="*60)
    print("STTIMS DATA VERIFICATION")
    print("="*60)
    
    # Users
    print("\n👤 USERS:")
    users = User.query.all()
    print(f"  Total: {len(users)}")
    for u in users:
        print(f"  - ID:{u.user_id} | {u.username} | {u.role} | {u.email}")
    
    # Trainees
    print("\n👨‍🎓 TRAINEES:")
    trainees = Trainee.query.all()
    print(f"  Total: {len(trainees)}")
    for t in trainees[:5]:
        print(f"  - ID:{t.trainee_id} | {t.first_name} {t.last_name} | {t.email}")
    
    # Instructors
    print("\n👨‍🏫 INSTRUCTORS:")
    instructors = Instructor.query.all()
    print(f"  Total: {len(instructors)}")
    for i in instructors[:5]:
        print(f"  - ID:{i.instructor_id} | {i.first_name} {i.last_name} | {i.email}")
    
    # Categories
    print("\n📂 CATEGORIES:")
    categories = Category.query.all()
    print(f"  Total: {len(categories)}")
    for c in categories:
        print(f"  - ID:{c.category_id} | {c.category_name} | {c.category_code}")
    
    # Courses
    print("\n📚 COURSES:")
    courses = Course.query.all()
    print(f"  Total: {len(courses)}")
    for c in courses:
        print(f"  - ID:{c.course_id} | {c.course_code} | {c.course_title}")
    
    # Batches
    print("\n📅 BATCHES:")
    batches = Batch.query.all()
    print(f"  Total: {len(batches)}")
    for b in batches:
        print(f"  - ID:{b.batch_id} | {b.batch_code} | {b.batch_name}")
    
    # Enrollments
    print("\n📝 ENROLLMENTS:")
    enrollments = Enrollment.query.all()
    print(f"  Total: {len(enrollments)}")
    for e in enrollments[:5]:
        print(f"  - ID:{e.enrollment_id} | Trainee:{e.trainee_id} | Batch:{e.batch_id}")
    
    print("\n" + "="*60)
    print("✅ Data verification complete!")
    print("="*60)
