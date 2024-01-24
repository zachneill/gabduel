"""This file contains the tests for the accounts logic functions"""
import pytest

from app.logic.accounts import createUser


def test_Users(newUser):
    """Test the SQLAlchemy User class exists and has the correct attributes"""
    assert newUser.email == 'email'
    assert newUser.firstName == 'FN'
    assert newUser.lastName == 'LN'
    assert newUser.username == 'username'
    assert newUser.password == 'password'
    assert not newUser.isAdmin


def test_createUser(newUser):
    """Test the createUser function
        It should create a new user with the correct attributes
    """
    # Create a test user
    newUser = createUser(
        {'email': 'email', 'firstName': 'FN', 'lastName': 'LN', 'username': 'username', 'password': 'password',
         'isAdmin': False})
    # Check the attributes
    assert newUser.email == 'email'
    assert newUser.firstName == 'FN'
    assert newUser.lastName == 'LN'
    assert newUser.username == 'username'
    assert not newUser.isAdmin
    # Check the password is hashed
    assert newUser.password.exists()


def test_createUserNoAttributes(newUser):
    """Test the createUser function
        It should not create a new user if not enough attributes are provided
        """
    # Test with no email
    with pytest.raises(TypeError):
        createUser(
            {'firstName': 'FN', 'lastName': 'LN', 'username': 'username', 'password': 'password',
             'isAdmin': False})
    # Test with no first name
    with pytest.raises(TypeError):
        createUser(
            {'email': "abc@abc.com", 'lastName': 'LN', 'username': 'username', 'password': 'password',
             'isAdmin': False})
    # Test with no last name
    with pytest.raises(TypeError):
        createUser(
            {'email': "abc@abc.com", 'firstName': 'FN', 'username': 'username', 'password': 'password',
             'isAdmin': False})
    # Test with no username
    with pytest.raises(TypeError):
        createUser(
            {'email': "abc@abc.com", 'firstName': 'FN', 'lastName': 'LN', 'password': 'password',
             'isAdmin': False})
    # Test with no password
    with pytest.raises(TypeError):
        createUser(
            {'email': "abc@abc.com", 'firstName': 'FN', 'lastName': 'LN', 'username': 'username',
             'isAdmin': False})
    # Test with no isAdmin, which should default to False
    createUser(
        {'email': "abc@abc.com", 'firstName': 'FN', 'lastName': 'LN', 'username': 'username',
         'password': 'password'})
    assert not newUser.isAdmin
