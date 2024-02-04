"""This file contains the Post object for the database"""
from datetime import datetime

from app.models.objects.post_authors import postAuthors
from database import db


class Post(db.Model):
    """Post model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="Untitled Post")
    content = db.Column(db.String(3000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now())
    intensity = db.Column(db.Integer, nullable=False, default=1)
    type = db.Column(db.String(10), nullable=False, default='Duel')
    authors = db.relationship('User', secondary=postAuthors,
                              back_populates="posts", passive_deletes=True, lazy=True)
    supports = db.relationship('Support', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.id}', '{self.title}', '{self.type}', '{self.authors}')"
