"""This file contains the logic functions for the posts"""
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from app.models.objects.post import Post
from app.models.objects.user import User
from database import db


def createPost(data):
    """Create a new post"""
    try:
        newPost = Post(title=data['title'], content=data['content'], intensity=data['intensity'],
                       type=data['type'], supported1=0, supported2=0)
        db.session.add(newPost)
        author1 = db.session.get(User, data['authors'][0])
        author2 = db.session.get(User, data['authors'][1])
        newPost.authors.append(author1)
        newPost.authors.append(author2)
        author1.postCount += 1
        author2.postCount += 1
        db.session.commit()
    except Exception as e:
        print("Failed to create post with error: ", e)
        raise SQLAlchemyError

    return newPost


def getPosts():
    """Get all posts, sorted newest to oldest"""
    return Post.query.order_by(Post.date.desc())


def getUserPosts(user):
    """Get all posts by a user"""
    return Post.query.filter(Post.authors.contains(user)).order_by(Post.date.desc())


def getPostById(postId):
    """Get a post by its id"""
    return Post.query.filter_by(id=postId).first()


def updatePost(data):
    """Update a post"""
    try:
        post = db.session.get(Post, data['id'])
        post.title = data['title']
        post.content = data['content']
        post.intensity = data['intensity']
        post.type = data['type']
        author1 = db.session.get(User, data['authors'][0])
        author2 = db.session.get(User, data['authors'][1])
        post.authors.clear()
        post.authors.append(author1)
        post.authors.append(author2)
        db.session.commit()
    except Exception as e:
        print("Failed to update post with error: ", e)
        raise SQLAlchemyError

    return post


def supportAuthor(postId, supportId, mindChanged):
    """Support an author"""
    try:
        post = db.session.get(Post, postId)
        author1 = post.authors[0]
        author2 = post.authors[1]
        if supportId == 1:
            post.supported1 += 1
            author1.supports += 1
        else:
            post.supported2 += 1
            author2.supports += 1
        if mindChanged:
            if supportId == 1:
                post.supported2 -= 1
                author2.supports -= 1
            else:
                post.supported1 -= 1
                author1.supports -= 1
        db.session.commit()
    except Exception as e:
        print("Failed to support author with error: ", e)
        raise SQLAlchemyError

    return post


def deletePost(data):
    """Delete a post"""
    try:
        post = Post.query.filter_by(id=data['id']).first()
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        print("Failed to delete post with error: ", e)
        raise NoResultFound

    return post


def getSearchResults(query):
    """Get the search results"""
    return Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).order_by(Post.date.desc())


