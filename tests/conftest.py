import pytest

from app import create_app
from app.models.objects.post import Post
from app.models.objects.user import User as Users
from database import db


@pytest.fixture(scope='module')
def testClient(newUser, secondUser, newPost, secondPost):
    """Fixture for functional tests. Creates a test client for the application."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as testingClient:
        # Establish an application context before running the tests
        with app.app_context():
            db.create_all()
            db.session.add(newUser)
            db.session.add(secondUser)
            db.session.add(newPost)
            db.session.add(secondPost)
            db.session.add(Post(title='title2', content='content2', author=2))
            yield testingClient
            db.drop_all()


@pytest.fixture(scope='module')
def newUser():
    """Fixture for unit tests. Creates a new user object."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        user = Users()
        user.id = 1
        user.email = 'email@email.com'
        user.firstName = 'FN'
        user.lastName = 'LN'
        user.username = 'username'
        user.password = 'password'
        user.isAdmin = False
        db.session.add(user)
    return user


@pytest.fixture(scope='module')
def secondUser():
    """For when two users are needed, or a user whose password is hashed."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        user = Users()
        user.id = 2
        user.email = 'email2@email.com'
        user.firstName = 'FN'
        user.lastName = 'LN'
        user.username = 'username2'
        user.password = 'scrypt:32768:8:1$fajWmZeuTbMKdz7r$609c9395583ceffcdd714c5656794cb7c088de2af874cdb898c75d1c17145b1f8c03878bcd800435026fcf5989f6373a4b7f8b046d2f6c17810662842a3ecafc'
        user.isAdmin = False
        db.session.add(user)
    return user


@pytest.fixture(scope='module')
def newPost(newUser):
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        """Fixture for unit tests. Creates a new post object."""
        post = Post()
        post.title = 'title'
        post.content = 'content'
        post.author = newUser.id
        db.session.add(post)
    return post


@pytest.fixture(scope='module')
def secondPost(newUser, secondUser):
    """For when two posts are needed."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        post = Post()
        post.title = 'title2'
        post.content = 'content2'
        post.author = secondUser.id
        db.session.add(post)
    return post

