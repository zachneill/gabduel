"""This file contains the Support object for the database"""

from flask_login import UserMixin

from database import db


class Support(db.Model, UserMixin):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    authorId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    supporterId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    userAuthorId = db.relationship("User", backref="authorId", foreign_keys=[authorId])
    userSupporterId = db.relationship("User", backref="supporterId", foreign_keys=[supporterId])


    # def __repr__(self):
    #     return f"Support('{self.postId}', '{self.authorId}', '{self.supporterId}')"
