from app.models.objects.post import Post
from database import db


def createPost(data):
    newPost = Post(title=data['title'], content=data['content'], authorId=data['authorId'])
    db.session.add(newPost)
    db.session.commit()
    return newPost
