"""This file contains the tests for the accounts logic functions"""
import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.logic.accounts import createUser, checkPassword, getUserByEmail, getUserByUsername, getUserById, getUsers
from database import db


def test_Users(newUser):
    """Test the SQLAlchemy User class exists and has the correct attributes"""
    assert newUser.email == 'email@email.com'
    assert newUser.firstName == 'FN'
    assert newUser.lastName == 'LN'
    assert newUser.username == 'username'
    assert newUser.password == 'password'
    assert not newUser.isAdmin


def test_createUser(testClient):
    """Test the createUser function
        It should create a new user with the correct attributes
    """
    # Create a test user
    user = createUser(
        {'email': 'email3@email.com', 'firstName': 'FN', 'lastName': 'LN', 'username': 'username3',
         'password': 'password', 'isAdmin': False})
    # Check the attributes
    assert user.email == 'email3@email.com'
    assert user.firstName == 'FN'
    assert user.lastName == 'LN'
    assert user.username == 'username3'
    assert not user.isAdmin
    # Check the password is hashed
    assert isinstance(user.password, str)


def test_createUserNoAttributes(newUser):
    """Test the createUser function
        It should not create a new user if not enough attributes are provided
        """
    # Test with no email
    with pytest.raises(SQLAlchemyError):
        createUser(
            {'firstName': 'FN', 'lastName': 'LN', 'username': 'username', 'password': 'password',
             'isAdmin': False})
    # Test with no first name
    with pytest.raises(SQLAlchemyError):
        createUser(
            {'email': "abc@abc.com", 'lastName': 'LN', 'username': 'username', 'password': 'password',
             'isAdmin': False})
    # Test with no last name
    with pytest.raises(SQLAlchemyError):
        createUser(
            {'email': "abc@abc.com", 'firstName': 'FN', 'username': 'username', 'password': 'password',
             'isAdmin': False})
    # Test with no username
    with pytest.raises(SQLAlchemyError):
        createUser(
            {'email': "abc@abc.com", 'firstName': 'FN', 'lastName': 'LN', 'password': 'password',
             'isAdmin': False})
    # Test with no password
    with pytest.raises(SQLAlchemyError):
        createUser(
            {'email': "abc@abc.com", 'firstName': 'FN', 'lastName': 'LN', 'username': 'username',
             'isAdmin': False})
    # Test with no isAdmin
    with pytest.raises(SQLAlchemyError):
        createUser(
            {'email': "abc@abc.com", 'firstName': 'FN', 'lastName': 'LN', 'username': 'username',
             'password': 'password'})


def test_checkPassword(secondUser):
    """Test the checkPassword function
        It should return True if the password is correct
    """
    # Check the password is correct
    assert checkPassword(secondUser.password, 'password')
    # Check the password is incorrect
    assert not checkPassword(secondUser.password, 'wrongpassword')


def test_getUserByEmail(testClient, newUser):
    """Test the getUserByEmail function
        It should return the correct user
    """
    # Check the user is returned
    assert newUser == getUserByEmail('email@email.com')
    # Check the user is not returned
    assert not getUserByEmail('wrongemail@email.com')


def test_getUserByUsername(testClient, newUser):
    """Test the getUserByUsername function
        It should return the correct user
    """
    # Check the user is returned
    assert newUser == getUserByUsername('username')
    # Check the user is not returned
    assert not getUserByUsername('wrongusername')


def test_getUserById(testClient, newUser):
    """Test the getUserById function
        It should return the correct user
    """
    # Check the user is returned
    assert newUser == getUserById(newUser.id)
    # Check the user is not returned
    assert not getUserById(999)


def test_getUsers(newUser, secondUser, testClient):
    """Test the getUsers function
        It should return all users
    """
    # Check the users are returned
    assert newUser in getUsers()
    assert secondUser in getUsers()
    # Check the correct user objects are returned
    assert [newUser, newUser] != getUsers()


def makeAdmin(newUser):
    """Test the makeAdmin function
        It should make the user an admin
    """
    # Check the user is not an admin
    assert not newUser.isAdmin
    # Make the user an admin
    makeAdmin(newUser.id)
    # Check the user is an admin
    assert newUser.isAdmin
