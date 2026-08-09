#!/bin/bash

cd ~/Documents/sttims
source venv/bin/activate

echo "=========================================="
echo "🗑️  Resetting STTIMS Database"
echo "=========================================="

# Drop and recreate database
echo "📊 Dropping and recreating database..."
sudo mysql -u root -e "DROP DATABASE IF EXISTS sttims_db; CREATE DATABASE sttims_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# Create tables
echo "📊 Creating tables..."
python3 << 'PYEOF'
from app import app
from models import db

with app.app_context():
    db.create_all()
    print("✅ Tables created successfully!")
    
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📋 Tables: {', '.join(tables)}")
PYEOF

# Create users
echo "👤 Creating users..."
python3 << 'PYEOF'
from app import app
from models import db, User

with app.app_context():
    users = [
        ('admin', 'admin@sttims.com', 'Admin', 'Admin123!'),
        ('manager', 'manager@sttims.com', 'Manager', 'Manager123!'),
        ('instructor', 'instructor@sttims.com', 'Instructor', 'Instructor123!'),
        ('trainee', 'trainee@sttims.com', 'Trainee', 'Trainee123!'),
    ]
    
    for username, email, role, password in users:
        user = User(username=username, email=email, role=role, status='Active')
        user.set_password(password)
        db.session.add(user)
    
    db.session.commit()
    print(f"✅ Created {len(users)} users")
    
    # Show users
    all_users = User.query.all()
    print("\n📋 Users:")
    for u in all_users:
        print(f"   - {u.username} ({u.role})")
PYEOF

echo ""
echo "=========================================="
echo "✅ Reset complete!"
echo "=========================================="
echo "🔑 Login Credentials:"
echo "   Admin:      admin / Admin123!"
echo "   Manager:    manager / Manager123!"
echo "   Instructor: instructor / Instructor123!"
echo "   Trainee:    trainee / Trainee123!"
echo "=========================================="
echo ""
echo "🚀 Starting Flask server..."
python app.py
