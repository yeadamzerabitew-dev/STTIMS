from app import create_app, db
from models import User

app = create_app()

with app.app_context():
    admin = User(username='admin', email='admin@sttims.com', role='Admin', status='Active')
    admin.set_password('Admin123!')
    db.session.add(admin)
    
    manager = User(username='manager', email='manager@sttims.com', role='Manager', status='Active')
    manager.set_password('Manager123!')
    db.session.add(manager)
    
    instructor = User(username='instructor', email='instructor@sttims.com', role='Instructor', status='Active')
    instructor.set_password('Instructor123!')
    db.session.add(instructor)
    
    trainee = User(username='trainee', email='trainee@sttims.com', role='Trainee', status='Active')
    trainee.set_password('Trainee123!')
    db.session.add(trainee)
    
    db.session.commit()
    print("✅ Test users created successfully!")
    print("\n📋 Test Credentials:")
    print("   Admin:      admin / Admin123!")
    print("   Manager:    manager / Manager123!")
    print("   Instructor: instructor / Instructor123!")
    print("   Trainee:    trainee / Trainee123!")
