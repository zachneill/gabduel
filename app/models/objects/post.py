"""This file contains the Post object for the database"""
from datetime import datetime

from app.models.objects.postAuthors import postAuthors
from database import db


class Post(db.Model):
    """Post model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="Untitled Post")
    content = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now())
    intensity = db.Column(db.Integer, nullable=False, default=1)
    authors = db.relationship('User', secondary=postAuthors,
                              back_populates="posts", passive_deletes=True, lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', {self.content}, '{self.date}')"
