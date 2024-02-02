"""This file contains the logic functions for the posts"""
from sqlalchemy import func, text
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from app.models.objects.post import Post
from app.models.objects.support import Support
from app.models.objects.user import User
from database import db


def createPost(data):
    """Create a new post"""
    try:
        newPost = Post(title=data['title'], content=data['content'], intensity=data['intensity'],
                       type=data['type'])
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


def getSupportsByPost(postId):
    """Get the number of supports for a post"""
    return Support.query.filter(Support.postId == postId)


def getPostSupportsCountById(postId):
    """Get the number of supports for a post"""
    return (Support.query.filter(Support.postId == postId)).count()


def getUserSupportedPostsById(userId):
    return Support.query.filter(Support.supporterId == userId).all()


def getUserSupportedPostsCountById(userId):
    return (Support.query.filter(Support.authorId == userId)).count()


def getPosts():
    """Get all posts, sorted newest to oldest"""
    return Post.query.order_by(Post.date.desc())


def getUserPosts(user):
    """Get all posts by a user"""
    return Post.query.filter(Post.authors.contains(user)).order_by(Post.date.desc())


def getSpecialPosts(kind, query):
    """ Filters post by type and intensity """
    try:
        if query == 'newest':
            # Get all posts, sorted newest to oldest
            return Post.query.order_by(Post.date.desc())
        elif query == 'oldest':
            # Get all posts, sorted oldest to newest
            return Post.query.order_by(Post.date.asc())
        # Check if filtering by gab or duel
        if kind == 'gabs':
            type = 'gab'
        else:
            type = "duel"
        if query == "support":
            # Get all posts of type "gab"
            posts = db.session.query(Post, func.count(Post.supports).label('total')) \
                .join(Post.supports).group_by(Post).order_by(text('total DESC'))
            posts = sorted(posts, key=lambda x: x[1], reverse=True)
            postIds = [post[0].id for post in posts]
            posts = Post.query.filter(type == type, Post.id.in_(postIds))
            return posts
        else:
            # Get posts, sorted by intensity
            return Post.query.filter_by(type=type).order_by(Post.intensity.desc())
    except Exception as e:
        print("Failed to get special posts with error: ", e)
        raise SQLAlchemyError


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


def createSupport(authorId, supporterId, postId):
    newSupport = Support()
    newSupport.supporterId = supporterId
    newSupport.authorId = authorId
    newSupport.postId = postId
    db.session.add(newSupport)
    db.session.commit()
    return newSupport


def removeSupport(supporterId, postId):
    supportInstance = Support.query.filter_by(postId=postId, supporterId=supporterId).first()
    db.session.delete(supportInstance)


def supportAuthor(winnerId, supporterId, postId, mindChanged):
    """Support an author"""
    try:
        if mindChanged:
            removeSupport(supporterId, postId)
        newSupport = createSupport(winnerId, supporterId, postId)
        db.session.commit()
    except Exception as e:
        print("Failed to support author with error: ", e)
        raise SQLAlchemyError

    return newSupport


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
