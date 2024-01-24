from app.models.objects.post import Post
from app.models.objects.user import User
from database import db


def createPost(data):
    """Create a new post"""
    newPost = Post(title=data['title'], content=data['content'], author=data['author'])
    db.session.add(newPost)
    db.session.commit()
    return newPost


def getPosts():
    """Get all posts, sorted newest to oldest"""
    return Post.query.order_by(Post.date.desc()).all()
