from app.models.objects.user import User
from database import db
from werkzeug.security import generate_password_hash, check_password_hash


def createUser(data):
    """Create a new user"""
    newUser = User(email=data['email'], firstName=data['firstName'], lastName=data['lastName'],
                   username=data['username'], password=generate_password_hash(data['password'], method='scrypt'),
                   isAdmin=data['isAdmin'])
    db.session.add(newUser)
    db.session.commit()
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
    return User.query.get(int(userId))


def getUsers():
    """Get all users"""
    return User.query.all()


def makeAdmin(id):
    user = getUserById(id)
    user.isAdmin = True
    db.session.commit()
    return user
