from app import app
from models import db, User, Trainee, Instructor, Course, Batch, Enrollment, Category, GradeScale
import bcrypt
from datetime import datetime

def insert_data():
    with app.app_context():
        print("📊 Inserting sample data...")
        
        # Helper function to hash password
        def hash_password(password):
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        # 1. Add Admin User (if not exists)
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@sttims.com',
                password_hash=hash_password('Admin123!'),
                role='Admin',
                status='Active'
            )
            db.session.add(admin)
            print("✅ Admin user created")
        
        # 2. Add a test trainee (if not exists)
        trainee = Trainee.query.filter_by(email='test@email.com').first()
        if not trainee:
            trainee = Trainee(
                trainee_code='T-001',
                first_name='Test',
                last_name='User',
                email='test@email.com',
                phone_number='0912345678',
                status='Active'
            )
            db.session.add(trainee)
            db.session.flush()
            print("✅ Test trainee created")
            
            # Create user account for trainee
            trainee_user = User(
                username='test',
                email='test@email.com',
                password_hash=hash_password('Test123!'),
                role='Trainee',
                trainee_id=trainee.id,
                status='Active'
            )
            db.session.add(trainee_user)
            print("✅ Trainee user created")
        
        # 3. Add a test instructor (if not exists)
        instructor = Instructor.query.filter_by(email='instructor@test.com').first()
        if not instructor:
            instructor = Instructor(
                instructor_code='INS-001',
                first_name='Test',
                last_name='Instructor',
                email='instructor@test.com',
                phone_number='0923456789',
                qualification='PhD in Test',
                years_of_experience=5,
                status='Active',
                employment_type='Full Time',
                joining_date=datetime.now(),
                department='IT'
            )
            db.session.add(instructor)
            db.session.flush()
            print("✅ Test instructor created")
            
            # Create user account for instructor
            instructor_user = User(
                username='instructor',
                email='instructor@test.com',
                password_hash=hash_password('Instructor123!'),
                role='Instructor',
                instructor_id=instructor.id,
                status='Active'
            )
            db.session.add(instructor_user)
            print("✅ Instructor user created")
        
        # Commit all changes
        db.session.commit()
        
        # Show summary
        print("\n" + "="*50)
        print("✅ DATA INSERTION COMPLETE!")
        print("="*50)
        print(f"📊 Users: {User.query.count()}")
        print(f"📊 Trainees: {Trainee.query.count()}")
        print(f"📊 Instructors: {Instructor.query.count()}")
        print(f"📊 Courses: {Course.query.count()}")
        print(f"📊 Batches: {Batch.query.count()}")
        print(f"📊 Enrollments: {Enrollment.query.count()}")
        print("="*50)
        
        print("\n🔑 Login Credentials:")
        print("  Admin:      admin / Admin123!")
        print("  Trainee:    test / Test123!")
        print("  Instructor: instructor / Instructor123!")
        print("\n✅ All done!")

if __name__ == "__main__":
    insert_data()
