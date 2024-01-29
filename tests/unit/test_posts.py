"""This file contains the unit tests for the posts logic functions"""
import pytest
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from app.logic.posts import createPost, getPosts, getPostById, updatePost, deletePost, supportAuthor, getSpecialPosts


def test_supportAuthor(newPost, newUser, secondUser, unitContext):
    """ Test the supportAuthor function"""
    # Support author 1
    post = supportAuthor(newPost.id, 1, False)
    assert post.supported1 == 2
    assert post.supported2 == 0
    assert newUser.supports == 2
    assert secondUser.supports == 0
    # Support author 2
    post = supportAuthor(newPost.id, 2, False)
    assert post.supported1 == 2
    assert post.supported2 == 1
    assert newUser.supports == 2
    assert secondUser.supports == 1
    # Change mind
    post = supportAuthor(newPost.id, 1, True)
    assert post.supported1 == 3
    assert post.supported2 == 0
    assert newUser.supports == 3
    assert secondUser.supports == 0
    # Change mind again
    post = supportAuthor(newPost.id, 2, True)
    assert post.supported1 == 2
    assert post.supported2 == 1
    assert newUser.supports == 2
    assert secondUser.supports == 1
    # Test invalid post id
    with pytest.raises(SQLAlchemyError):
        supportAuthor(0, 1, False)


def test_getSpecialPosts(newPost, secondPost, unitContext):
    """Test the getSpecialPosts function
        It should return the correct posts
    """
    # Test newest, should return all posts sorted newest to oldest
    posts = getSpecialPosts('gabs', 'newest')
    assert posts[0] == newPost
    # Test oldest, should return all posts sorted oldest to newest
    posts = getSpecialPosts('gabs', 'oldest')
    assert posts[1] == secondPost


def test_createPost(newUser, secondUser, unitContext):
    """Test the createPost function
        It should create a new post with the correct attributes
    """
    # Create a test post
    post = createPost({'title': 'title', 'content': 'content', 'intensity': 2,
                       'authors': [newUser.id, secondUser.id], 'type': 'gab'})
    # Check the attributes
    assert post.title == 'title'
    assert post.content == 'content'
    assert post.type == "gab"
    assert post.authors == [newUser, secondUser]


def test_createPostNoAttributes(newUser, unitContext, secondUser):
    """Test the createPost function
        It should not create a new post if not enough attributes are provided
    """
    # Test with no title
    with pytest.raises(SQLAlchemyError):
        createPost({'content': 'content', 'authors': [newUser.id, secondUser.id],
                    'intensity': 2, 'type': 'gab'})
    # Test with no content
    with pytest.raises(SQLAlchemyError):
        createPost({'title': 'title', 'authors': [newUser.id, secondUser.id],
                    'intensity': 2, 'type': 'gab'})
    # Test with no author
    with pytest.raises(SQLAlchemyError):
        createPost({'title': 'title', 'content': 'content',
                    'intensity': 2, 'type': 'gab'})
    # Test with no intensity
    with pytest.raises(SQLAlchemyError):
        createPost({'title': 'title', 'content': 'content', 'authors': [newUser.id, secondUser.id],
                    'type': 'gab'})
    # Test with no type
    with pytest.raises(SQLAlchemyError):
        createPost({'title': 'title', 'content': 'content', 'authors': [newUser.id, secondUser.id],
                    'intensity': 2})


def test_getPosts(newPost, secondPost):
    """Test the getPosts function
        It should return a list of all posts
    """
    # Check the returned list contains the fixture posts
    posts = getPosts()
    assert newPost in posts
    assert secondPost in posts


def test_getPostById(newPost):
    """Test the getPostById function
        It should return the correct post
    """
    # Check the returned post is the fixture post
    assert getPostById(newPost.id) == newPost
    # Check the function raises an error if the id is invalid
    assert not getPostById(0)


def test_updatePost(newPost, newUser, thirdUser, unitContext):
    """Test the updatePost function
        It should update the post with the correct attributes
    """
    # Update the post
    post = updatePost({'id': newPost.id, 'title': 'new title', 'content': 'new content',
                       'authors': [newUser.id, thirdUser.id], 'intensity': 5, 'type': 'duel'})
    # Check the attributes
    assert post.title == 'new title'
    assert post.content == 'new content'
    assert post.authors == [newUser, thirdUser]
    assert post.intensity == 5
    assert post.type == 'duel'


def test_updatePostNoAttributes(newPost):
    """Test the updatePost function
        It should not update the post if not enough attributes are provided
    """
    # Test with no id
    with pytest.raises(SQLAlchemyError):
        updatePost({'title': 'new title', 'content': 'new content', 'authors': [98, 99],
                    'intensity': 2, 'type': 'gab'})
    # Test with no title
    with pytest.raises(SQLAlchemyError):
        updatePost({'id': newPost.id, 'content': 'new content', 'authors': [98, 99],
                    'intensity': 2, 'type': 'gab'})
    # Test with no content
    with pytest.raises(SQLAlchemyError):
        updatePost({'id': newPost.id, 'title': 'new title', 'authors': [98, 99],
                    'intensity': 2, 'type': 'gab'})
    # Test with no authors
    with pytest.raises(SQLAlchemyError):
        updatePost({'id': newPost.id, 'title': 'new title', 'content': 'new content',
                    'intensity': 2, 'type': 'gab'})
    # Test with no intensity
    with pytest.raises(SQLAlchemyError):
        updatePost({'id': newPost.id, 'title': 'new title', 'content': 'new content',
                    'authors': [98, 99], 'type': 'gab'})
    # Test with no type
    with pytest.raises(SQLAlchemyError):
        updatePost({'id': newPost.id, 'title': 'new title', 'content': 'new content',
                    'authors': [98, 99], 'intensity': 2})


def test_deletePost(newPost, unitContext, app):
    """Test the deletePost function
        It should delete the post
    """
    with app.test_client() as testingClient:
        with app.app_context():
            # Delete the post
            post = deletePost({'id': newPost.id})
            # Check the post is deleted
            assert post not in getPosts()
            # Check the post doesn't work on invalid id
            with pytest.raises(NoResultFound):
                deletePost({'id': 0})