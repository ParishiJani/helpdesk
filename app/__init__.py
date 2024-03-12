from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import User
from .extensions import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config.from_pyfile('config.py')
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong, secret key
db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the user_loader function to load a user by ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import your routes and models
from app import routes, models
