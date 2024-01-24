from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship('Post')

    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', '{self.email}')"
