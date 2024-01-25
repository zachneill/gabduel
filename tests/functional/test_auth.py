import pytest
from flask import url_for


def test_login(app, newUser):
    """Test the login page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get(url_for('auth.login'), follow_redirects=False)
            assert response.status_code == 200
            assert b'Email' in response.data
            assert b'Password' in response.data
            # Send a POST request to the application
            response = testingClient.post(url_for('auth.login'),
                                          data=dict(email=newUser.email, password=newUser.password),
                                          follow_redirects=True)
            assert response.status_code == 200
            # assert b'This is Flask Blog' in response.data


def test_signup(app, newUser):
    """Test the signup page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get(url_for('auth.signup'), follow_redirects=False)
            assert response.status_code == 200
            assert b'First Name' in response.data
            assert b'Last Name' in response.data
            assert b'Username' in response.data
            assert b'Email' in response.data
            assert b'Password' in response.data
            assert b'Confirm Password' in response.data

            # Send a POST request to the application
            response = testingClient.post(url_for('auth.signup'),
                                          data=dict(firstName=newUser.firstName, lastName=newUser.lastName,
                                                    username=newUser.username, email=newUser.email,
                                                    password=newUser.password,
                                                    confirmPassword=newUser.password), follow_redirects=True)
            assert response.status_code == 200
            assert b'Account created for' in response.data


def test_logout(app):
    """Test the logout page."""
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            # Send a GET request to the application
            response = testingClient.get('/logout', follow_redirects=True)
            assert response.status_code == 200
            assert b'Email' in response.data
            assert b'Password' in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_post(app, newUser):
    """Test the post page."""
    with app.test_client() as testingClient:
        # Send a GET request to the application
        response = testingClient.get('/post', follow_redirects=True)
        assert response.status_code == 200
        assert b'Post' in response.data
        # Change email and username to avoid duplicate errors from lack of app context
        newUser.email = "email5@email.com"
        newUser.username = "username5"

        # Test the POST request version
        response = testingClient.post('/post', follow_redirects=True, data={'content': 'content', 'title': 'title'})
        assert response.status_code == 200
        assert b'Post created!' in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_update(app):
    """Test the update page."""
    with app.test_client() as testingClient:
        # Send a GET request to the application
        response = testingClient.get('/post/1')
        assert response.status_code == 200
        assert b'Update' in response.data

        # Test the POST request version
        response = testingClient.post('/post/1', follow_redirects=True, data={'content': 'content', 'title': 'title'})
        assert response.status_code == 200
        assert b'Post updated!' in response.data


def test_delete(app, newPost):
    """Test the delete functionality."""
    with app.test_client() as testingClient:
        # Send a POST request to the application
        response = testingClient.post('/delete', data={'postId':  newPost.id}, follow_redirects=True)
        assert response.status_code == 200
        assert b'This is the Flask Blog' in response.data
        assert b'title1' not in response.data


@pytest.mark.usefixtures("authenticated_request")
def test_non_admin(app):
    """Test the admin page."""
    with app.test_client() as testingClient:
        # Send a GET request to the application
        response = testingClient.get('/admin')

        assert response.status_code == 200
        assert b'You are not an admin' in response.data


@pytest.mark.usefixtures("admin_authenticated_request")
def test_admin(app):
    """Test the admin page."""
    with app.test_client() as testingClient:
        # Send a GET request to the application
        response = testingClient.get('/admin')
        assert response.status_code == 200
        assert b'All Users' in response.data
