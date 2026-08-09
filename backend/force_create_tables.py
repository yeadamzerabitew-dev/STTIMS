#!/usr/bin/env python
"""Force create all tables"""

from app import app
from models import db
from sqlalchemy import inspect

with app.app_context():
    print("📊 Creating all tables...")
    
    # Drop all tables first (optional - be careful!)
    # db.drop_all()
    
    # Create all tables
    db.create_all()
    
    # Verify tables were created
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print(f"\n✅ Tables created ({len(tables)}):")
    for table in tables:
        print(f"   - {table}")
    
    if len(tables) == 0:
        print("\n❌ No tables were created! Checking database connection...")
        try:
            db.session.execute(text("SELECT 1"))
            print("✅ Database connection is working")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
