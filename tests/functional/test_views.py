from flask import url_for


def test_404(app):
    """Test the 404 page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get('/404')
            assert response.status_code == 404
            assert b'404 Not Found' in response.data


def test_about(app):
    """Test the about page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get(url_for('views.home'), follow_redirects=True)
            assert response.status_code == 200
            # assert b'The Flask Blog is an established organization' in response.data


def test_home(app):
    """Test the home page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get(url_for('views.home'), follow_redirects=True)
            assert response.status_code == 200
            # assert b'This is Flask Blog' in response.data


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
