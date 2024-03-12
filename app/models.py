from datetime import datetime
from .extensions import db
from flask_login import UserMixin

#Python file for the database created 

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    tickets = db.relationship("Ticket", backref="User", foreign_keys="Ticket.user_id")

    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


# Ticket Model
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="WAITING")
    notes = db.Column(db.String(500), nullable=False, default='')

    def get_title_status(self):
        return self.status.replace("_", " ").title()

    def __repr__(self):
        return f"Ticket('{self.title}', '{self.created_at}')"
