"""This file contains the User object for the database"""
from datetime import datetime

from flask_login import UserMixin

from app.models.objects.post_authors import postAuthors
from database import db


class User(db.Model, UserMixin):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    isAdmin = db.Column(db.Boolean, nullable=False, default=False)
    image = db.Column(db.String(200), nullable=False,
                      default='https://api.dicebear.com/7.x/micah/svg?seed=abc&mouth=smile')
    joined = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now())
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    postCount = db.Column(db.Integer, nullable=False, default=0)
    posts = db.relationship('Post', secondary=postAuthors, back_populates="authors",
                            passive_deletes=True, lazy=True, cascade='all, delete')

    def __repr__(self):
        return f"User(''{self.id}'), {self.firstName}', '{self.lastName}', '{self.posts}')...etc"
