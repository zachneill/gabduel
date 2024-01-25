"""This file contains the unit tests for the posts logic functions"""
import pytest
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from app.logic.posts import createPost, getPosts, getPostById, updatePost, deletePost


def test_createPost(newUser, unitContext):
    """Test the createPost function
        It should create a new post with the correct attributes
    """
    # Create a test post
    post = createPost({'title': 'title', 'content': 'content', 'author': newUser.id})
    # Check the attributes
    assert post.title == 'title'
    assert post.content == 'content'
    assert post.author == newUser.id


def test_createPostNoAttributes(newUser, unitContext):
    """Test the createPost function
        It should not create a new post if not enough attributes are provided
    """
    # Test with no title
    with pytest.raises(SQLAlchemyError):
        createPost({'content': 'content', 'author': newUser.id})
    # Test with no content
    with pytest.raises(SQLAlchemyError):
        createPost({'title': 'title', 'author': newUser.id})
    # Test with no author
    with pytest.raises(SQLAlchemyError):
        createPost({'title': 'title', 'content': 'content'})


def test_getPosts(newPost, secondPost):
    """Test the getPosts function
        It should return a list of all posts
    """
    # Check the returned list contains the fixture posts
    assert newPost in getPosts()
    assert secondPost in getPosts()


def test_getPostById(newPost):
    """Test the getPostById function
        It should return the correct post
    """
    # Check the returned post is the fixture post
    assert getPostById(newPost.id) == newPost
    # Check the function raises an error if the id is invalid
    assert not getPostById(0)


def test_updatePost(newPost):
    """Test the updatePost function
        It should update the post with the correct attributes
    """
    # Update the post
    post = updatePost({'id': newPost.id, 'title': 'new title', 'content': 'new content'})
    # Check the attributes
    assert post.title == 'new title'
    assert post.content == 'new content'
    assert post.author == newPost.author


def test_updatePostNoAttributes(newPost):
    """Test the updatePost function
        It should not update the post if not enough attributes are provided
    """
    # Test with no id
    with pytest.raises(NoResultFound):
        updatePost({'title': 'new title', 'content': 'new content'})
    # Test with no title
    with pytest.raises(NoResultFound):
        updatePost({'id': newPost.id, 'content': 'new content'})
    # Test with no content
    with pytest.raises(NoResultFound):
        updatePost({'id': newPost.id, 'title': 'new title'})


def test_deletePost(newPost, unitContext):
    """Test the deletePost function
        It should delete the post
    """
    # Delete the post
    post = deletePost({'id': newPost.id})
    # Check the post is deleted
    assert post not in getPosts()
    # Check the post doesn't work on invalid id
    with pytest.raises(NoResultFound):
        deletePost({'id': 0})
