from app.models.objects.user import User
from database import db
from werkzeug.security import generate_password_hash, check_password_hash


def createUser(data):
    newUser = User(email=data['email'], firstName=data['firstName'], lastName=data['lastName'],
                   username=data['username'], password=generate_password_hash(data['password'], method='scrypt'),
                   isAdmin=data['isAdmin'])
    db.session.add(newUser)
    db.session.commit()
    return newUser


def checkPassword(passwordindb, userinput):
    return check_password_hash(passwordindb, userinput)


def getUserByEmail(email):
    return User.query.filter_by(email=email).first()


def getUserByUsername(username):
    return User.query.filter_by(username=username).first()


def getUserById(id):
    return User.query.get(int(id))
