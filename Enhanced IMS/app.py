
import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from models import db, login_manager

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key_123")  # Default for development

# SQLite configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = os.environ.get("CSRF_SECRET_KEY", "csrf_key_123")

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize extensions with app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from routes import *  # Import routes after app initialization

with app.app_context():
    db.create_all()
