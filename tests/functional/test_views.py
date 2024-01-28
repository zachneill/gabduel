"""This file contains the functional tests for the views."""
from flask import url_for


def test_about(app):
    """Test the about page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get(url_for('views.about'), follow_redirects=True)
            assert response.status_code == 200
            assert b'combine casual discussion' in response.data


def test_home(app):
    """Test the home page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get(url_for('views.home'), follow_redirects=True)
            assert response.status_code == 200
            assert b'This is Gab/Duel' in response.data
            # Test search bar post request from the home page
            response = testingClient.post(url_for('views.home'), follow_redirects=True, data=dict(search='test'))


def test_search(app):
    """Test the search results page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            # Test the search bar get request
            response = testingClient.get(url_for('views.search', query='test'), follow_redirects=True)
            assert response.status_code == 200
            assert b'Search Results' in response.data
            # Test the search bar post request from the search page
            response = testingClient.post("/search/test", follow_redirects=True, data=dict(search='test'))
            assert response.status_code == 200
            assert b'Search Results' in response.data


def test_404(app):
    """Test the 404 page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get('/404')
            assert response.status_code == 404
            assert b'404 Not Found' in response.data

            response = testingClient.get('/fake', follow_redirects=True)
            assert response.status_code == 404
            assert b'404 Not Found' in response.data


def test_500(app):
    """Test the 404 page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get('/500')
            assert response.status_code == 500
            assert b'500 Internal Server Error' in response.data


def test_405(app):
    """Test the 404 page."""
    # Send a GET request to the application
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            response = testingClient.get('/405')
            assert response.status_code == 405
            assert b'405 Method Not Allowed' in response.data
