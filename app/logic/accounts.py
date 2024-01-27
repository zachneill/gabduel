"""This file contains the logic for functions related to accounts"""
import os
import uuid
from flask import url_for
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from app.models.objects.post import Post
from app.models.objects.user import User
from database import db


def createUser(data):
    """Create a new user"""
    try:
        # Save the image to the static folder
        if data['image']:
            data['image'].save(os.path.join('app/static/images/avatars', secure_filename(data['username'] + '.png')))
            filename = url_for('static', filename='images/avatars/' + data['username'] + '.png')
        else:
            # If no image is provided, use the dicebear API to generate an avatar
            filename = f'https://api.dicebear.com/7.x/micah/svg?seed={str(uuid.uuid4())[:7]}&mouth=smile&eyes=smiling'

        newUser = User(email=data['email'], firstName=data['firstName'], lastName=data['lastName'],
                       username=data['username'], password=generate_password_hash(data['password'], method='scrypt'),
                       isAdmin=data['isAdmin'], image=filename)
        db.session.add(newUser)
        db.session.commit()
    except Exception as e:
        print("Failed to create user with error: ", e)
        raise SQLAlchemyError
    return newUser


def checkPassword(password, userinput):
    """Check if the input password is correct with the database"""
    return check_password_hash(password, userinput)


def getUserByEmail(email):
    """Get a user by their email address"""
    return User.query.filter_by(email=email).first()


def getUserByUsername(username):
    """Get a user by their username"""
    return User.query.filter_by(username=username).first()


def getUserById(userId):
    """Get a user by their id"""
    return db.session.get(User, userId)


def getUsers():
    """Get all users"""
    return User.query.all()


def makeAdmin(userId):
    user = db.session.get(User, userId)
    user.isAdmin = True
    db.session.commit()
    return user


def getAuthors():
    """Get all authors"""
    query = User.query.join(Post.authors).group_by(User.id).having(func.count(Post.id) > 0).all()
    return query
