from app.models.objects.post import Post
from app.models.objects.user import User
from database import db


def createPost(data):
    newPost = Post(title=data['title'], content=data['content'], author=data['author'])
    db.session.add(newPost)
    db.session.commit()
    return newPost


def getPosts():
    return Post.query.order_by(Post.date.desc()).all()
