from sqlalchemy import func

from database import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="Untitled Post")
    content = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    authorId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', {self.content}, '{self.date}')"