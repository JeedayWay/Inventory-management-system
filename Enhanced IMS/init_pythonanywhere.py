
"""
Run this file once on PythonAnywhere to initialize the database.
"""
from app import app, db
from models import User

with app.app_context():
    # Create tables
    db.create_all()
    
    # Check if admin user exists
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
        
    print("Database initialized successfully.")
