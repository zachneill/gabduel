# import pytest
#
#
# def test_login(testClient):
#     """Test the login page."""
#     # Send a GET request to the application
#     response = testClient.get('/login')
#     assert response.status_code == 200
#     assert b'Login' in response.data
#     assert b'Sign Up' in response.data
#
#
# def test_signup(testClient):
#     """Test the signup page."""
#     # Send a GET request to the application
#     response = testClient.get('/signup')
#     assert response.status_code == 200
#     assert b'Sign Up' in response.data
#
#
# def test_logout(testClient):
#     """Test the logout page."""
#     # Send a GET request to the application
#     response = testClient.get('/logout')
#     assert response.status_code == 302
#     assert b'Successfully logged out' in response.data
#
#
# def test_post(testClient):
#     """Test the post page."""
#     # Send a GET request to the application
#     response = testClient.get('/post')
#     assert response.status_code == 302
#     assert b'Create a Post' in response.data
#
#     # Test the POST request version
#     response = testClient.post('/post')
#     assert response.status_code == 302
#     assert b'Post created!' in response.data
#
#
# def test_update(testClient):
#     """Test the update page."""
#     # Send a GET request to the application
#     response = testClient.get('/post/1')
#     assert response.status_code == 302
#     assert b'Update Post' in response.data
#
#     # Test the POST request version
#     response = testClient.post('/post/1')
#     assert response.status_code == 302
#     assert b'Post updated!' in response.data
#
#
# def test_delete(testClient):
#     """Test the delete page."""
#     # Send a POST request to the application
#     response = testClient.post('/delete', data={'postId': 1})
#     assert response.status_code == 302
#     assert b'Post deleted!' in response.data
#
#
# def test_admin(testClient):
#     """Test the admin page."""
#     # Send a GET request to the application
#     response = testClient.get('/admin')
#     assert response.status_code == 302
#     assert b'Admin' in response.data