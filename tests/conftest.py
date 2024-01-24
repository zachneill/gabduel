import pytest
from app.models.objects.user import User
from app import create_app


@pytest.fixture(scope='module')
def newUser():
    """Fixture for unit tests. Creates a new user object."""
    user = User('email', 'FN', 'LN', 'username', 'password', False)
    return user


@pytest.fixture(scope='module')
def testClient():
    """Fixture for functional tests. Creates a test client for the application."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            yield testingClient
