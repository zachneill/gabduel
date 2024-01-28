"""This file contains the User object for the database"""
from flask_login import UserMixin

from app.models.objects.postAuthors import postAuthors
from database import db


class User(db.Model, UserMixin):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30), nullable=False)
    lastName = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    image = db.Column(db.String(20), nullable=False,
                      default='https://api.dicebear.com/7.x/micah/svg?seed=abc&mouth=smile')
    posts = db.relationship('Post', secondary=postAuthors,back_populates="authors",
                            passive_deletes=True, lazy=True)

    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', '{self.email}')"
