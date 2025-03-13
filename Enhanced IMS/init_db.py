
from app import app, db
from models import User, Category, Supplier
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
        
        # Add default categories
        categories = ['Electronics', 'Office Supplies', 'Furniture', 'Food & Beverages']
        for category_name in categories:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
        
        # Add a default supplier
        supplier = Supplier.query.filter_by(email='contact@acme.com').first()
        if not supplier:
            supplier = Supplier(
                name='ACME Supplies',
                contact_person='John Doe',
                email='contact@acme.com',
                phone='555-123-4567'
            )
            db.session.add(supplier)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
