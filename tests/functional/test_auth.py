"""This file contains the functional tests for the auth routes"""
import pytest
from flask import url_for


def test_login(app, secondUser, unitContext):
    """Test the login page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        with app.app_context():
            response = testingClient.get(url_for('auth.login'), follow_redirects=True)
            assert response.status_code == 200
            assert b'Email' in response.data
            assert b'Password' in response.data

            # Test no account exists with email
            response = testingClient.post(url_for('auth.login'),
                                          data=dict(login="fake@email.com", password="password"),
                                          follow_redirects=True)
            assert response.status_code == 200
            assert b"No account exists" in response.data

        # Test bad password
        response = testingClient.post(url_for('auth.login'),
                                      data=dict(login=secondUser.email, password="wrong"),
                                      follow_redirects=True)
        assert response.status_code == 200
        assert b"Incorrect password for" in response.data

        # Test login success
        response = testingClient.post(url_for('auth.login'),
                                      data=dict(login=secondUser.email, password="password"),
                                      follow_redirects=True)
        assert response.status_code == 200
        assert b"This is Folks Gab/Duel" in response.data


def test_signup_GET(app, unitContext):
    """Test the signup page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get(url_for('auth.signup'), follow_redirects=True)
            assert response.status_code == 200
            assert b'First Name' in response.data
            assert b'Last Name' in response.data
            assert b'Username' in response.data
            assert b'Email' in response.data
            assert b'Password' in response.data
            assert b'Confirm Password' in response.data


def test_signup_POST(app, newUser, unitContext):
    """Test the signup post requests."""
    with app.test_client() as testingClient:
        with app.app_context():
            # Test already existing email
            response = testingClient.post(url_for('auth.signup'),
                                          data=dict(firstName="test", lastName="test",
                                                    username="test2", email="email@email.com",
                                                    password="password", confirmPassword="password"),
                                          follow_redirects=True)
            assert response.status_code == 200
            assert b'already exists' in response.data
            # Test password mismatch
            response = testingClient.post(url_for('auth.signup'),
                                          data=dict(firstName="test", lastName="test",
                                                    username="test2", email="test2@test.com",
                                                    password="password", confirmPassword="password2"),
                                          follow_redirects=True)
            assert response.status_code == 200
            assert b'Passwords do not match.' in response.data

            # Test successful signup
            response = testingClient.post(url_for('auth.signup'),
                                          data=dict(firstName="test", lastName="test",
                                                    username="test", email="test@test.com",
                                                    password="password", confirmPassword="password"),
                                          follow_redirects=True)
            assert response.status_code == 200
            assert b'Account created for' in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_already_signed_up(app, unitContext):
    """Test if a user is already signed up."""
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        response = testingClient.get(url_for('auth.signup'), follow_redirects=True)
        assert response.status_code == 200
        assert b'This is Folks Gab/Duel' in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_already_logged_in(app, newUser):
    """Test if a user is already logged in."""
    with app.test_client() as testingClient:
        response = testingClient.get(url_for('auth.login'), follow_redirects=True)
        assert response.status_code == 200
        assert b'This is Folks Gab/Duel' in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_logout(app):
    """Test the logout page."""
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        response = testingClient.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Email' in response.data
        assert b'Password' in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_create_post(app):
    """Test the post page."""
    with app.test_client() as testingClient:
        # Send a GET request to the application
        response = testingClient.get('/post', follow_redirects=True)
        assert response.status_code == 200
        assert b'Post' in response.data
        # # Test successful post created
        response = testingClient.post('/post', follow_redirects=True, data={'content': 'content', 'title': 'title',
                                                                            'otherAuthor': [99]})
        assert response.status_code == 200
        assert b'Post created!' in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_update(app, newPost, secondPost):
    """Test the update page."""
    with app.test_client() as testingClient:
        # Send a GET request to the application
        response = testingClient.get(f'/post/{newPost.id}', follow_redirects=True)
        assert response.status_code == 200
        assert b'Update' in response.data

        # Test successful post updated
        response = testingClient.post(f'/post/{newPost.id}', follow_redirects=True,
                                      data={'content': 'new content', 'title': 'new title', 'otherAuthor':
                                          [99]})
        assert response.status_code == 200
        assert b'Post updated!' in response.data

        # Test changing someone else's post
        response = testingClient.post(f'/post/{secondPost.id}', follow_redirects=True,
                                      data={'content': 'new content', 'title': 'new title', 'otherAuthor':
                                          [99]})
        assert response.status_code == 200
        assert b'You are not the author' in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_delete(app, newPost):
    """Test the delete functionality."""
    # Send a POST request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        response = testingClient.post('/delete', data={'postId': newPost.id}, follow_redirects=True)
        assert response.status_code == 200
        assert b'This is Folks Gab/Duel' in response.data
        assert b'title1' not in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_cannot_delete(app, newPost, secondPost):
    """Test the delete functionality where you are not the author."""
    with app.test_client() as testingClient:
        # Test if you are not the author of the post
        response = testingClient.post('/delete', data={'postId': secondPost.id}, follow_redirects=True)
        assert response.status_code == 200
        assert b'title2' in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_non_admin(app, newUser):
    """Test the admin page."""
    with app.test_client() as testingClient:
        # Send a GET request to the application
        response = testingClient.get('/admin')

        assert response.status_code == 200
        assert b'You are not an admin' in response.data

        # Test making non-admin user an admin
        response = testingClient.post('/admin', data={'id': newUser.id}, follow_redirects=True)
        assert response.status_code == 200
        assert b'is now an admin' in response.data


@pytest.mark.usefixtures("admin_authenticated_request")
def test_admin(app):
    """Test the admin page."""
    with app.test_client() as testingClient:
        # Send a GET request to the application
        response = testingClient.get('/admin')
        assert response.status_code == 200
        assert b'All Users' in response.data
