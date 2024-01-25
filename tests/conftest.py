import flask_login
import pytest

from app import create_app
from app.models.objects.post import Post
from app.models.objects.user import User as Users, User
from database import db


@pytest.fixture(scope='module')
def app():
    """Fixture for functional tests. Inits the app."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture(autouse=True, scope='module')
def unitContext(app, newUser, secondUser, newPost, secondPost, adminUser):
    """Fixture for functional tests. Creates a test client for the application."""
    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            db.create_all()
            db.session.add(newUser)
            db.session.add(secondUser)
            db.session.add(adminUser)
            db.session.add(newPost)
            db.session.add(secondPost)
            yield testingClient
            db.drop_all()


@pytest.fixture(scope='module')
def newUser(app):
    """Fixture for unit tests. Creates a new user object."""
    with app.app_context():
        user = Users()
        user.id = 98
        user.email = 'email@email.com'
        user.firstName = 'FN'
        user.lastName = 'LN'
        user.username = 'username'
        user.password = 'password'
        user.isAdmin = False
        db.session.add(user)
    return user


@pytest.fixture(scope='module')
def secondUser(app):
    """For when two users are needed, or a user whose password is hashed."""
    with app.app_context():
        user = Users()
        user.id = 99
        user.email = 'email2@email.com'
        user.firstName = 'FN'
        user.lastName = 'LN'
        user.username = 'username2'
        user.password = 'scrypt:32768:8:1$fajWmZeuTbMKdz7r$609c9395583ceffcdd714c5656794cb7c088de2af874cdb898c75d1c17145b1f8c03878bcd800435026fcf5989f6373a4b7f8b046d2f6c17810662842a3ecafc'
        user.isAdmin = False
        db.session.add(user)
    return user


@pytest.fixture(scope='module')
def adminUser(app):
    """For when an admin user is needed."""
    with app.app_context():
        user = Users()
        user.id = 100
        user.email = 'admin@email.com'
        user.firstName = 'FN'
        user.lastName = 'LN'
        user.username = 'admin'
        user.password = 'password'
        user.isAdmin = True
        db.session.add(user)
    return user


@pytest.fixture(scope='module')
def newPost(app, newUser):
    """Fixture for unit tests. Creates a new post object."""
    with app.app_context():
        """Fixture for unit tests. Creates a new post object."""
        post = Post()
        post.title = 'title1'
        post.content = 'content1'
        post.author = newUser.id
        db.session.add(post)
    return post


@pytest.fixture(scope='module')
def secondPost(app, secondUser):
    """For when two posts are needed."""
    with app.app_context():
        post = Post()
        post.title = 'title2'
        post.content = 'content2'
        post.author = secondUser.id
        db.session.add(post)
    return post


@pytest.fixture
def authenticated_request(app, newUser):
    """Fixture for functional tests. Used as a decorator to log in."""
    with app.test_request_context():
        yield flask_login.login_user(newUser)


@pytest.fixture
def admin_authenticated_request(app, adminUser):
    """Fixture for functional tests. Used as a decorator to log in."""
    with app.test_request_context():
        yield flask_login.login_user(adminUser)
