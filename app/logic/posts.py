from app.models.objects.post import Post
from app.models.objects.user import User
from database import db


def createPost(data):
    """Create a new post"""
    try:
        newPost = Post(title=data['title'], content=data['content'], author=data['author'])
        db.session.add(newPost)
        db.session.commit()
    except Exception as e:
        print("Failed to create post with error", e)
        return None

    return newPost


def getPosts():
    """Get all posts, sorted newest to oldest"""
    return Post.query.order_by(Post.date.desc()).all()


def getPostById(postId):
    """Get a post by its id"""
    return Post.query.get(postId)


def updatePost(data):
    """Update a post"""
    try:
        post = Post.query.get(data['id'])
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
    except Exception as e:
        print("Failed to update post with error", e)
        return None

    return post


def deletePost(data):
    """Delete a post"""
    try:
        post = Post.query.get(data['id'])
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        print("Failed to delete post with error", e)
        return None

    return post
