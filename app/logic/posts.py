"""This file contains the logic functions for the posts"""
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from app.models.objects.post import Post
from database import db


def createPost(data):
    """Create a new post"""
    try:
        newPost = Post(title=data['title'], content=data['content'], author=data['author'])
        db.session.add(newPost)
        db.session.commit()
    except Exception as e:
        print("Failed to create post with error", e)
        raise SQLAlchemyError

    return newPost


def getPosts():
    """Get all posts, sorted newest to oldest"""
    return Post.query.order_by(Post.date.desc())


def getPostById(postId):
    """Get a post by its id"""
    return Post.query.filter_by(id=postId).first()


def updatePost(data):
    """Update a post"""
    try:
        post = Post.query.filter_by(id=data['id']).first()
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
    except Exception as e:
        print("Failed to update post with error", e)
        raise NoResultFound

    return post


def deletePost(data):
    """Delete a post"""
    try:
        post = Post.query.filter_by(id=data['id']).first()
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        print("Failed to delete post with error", e)
        raise NoResultFound

    return post


def getSearchResults(query):
    """Get the search results"""
    return Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).order_by(Post.date.desc())
