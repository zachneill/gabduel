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