# import pytest
#
#
# def test_home(testClient):
#     """Test the home page."""
#     # Send a GET request to the application
#     response = testClient.get('/')
#     assert response.status_code == 200
#     assert b'This is the Flask Blog' in response.data
#     # Test the other route to the home page
#     response = testClient.get('/home')
#     assert response.status_code == 200
#     assert b'This is the Flask Blog' in response.data
#     # Test inability to send a POST request to the home page
#     response = testClient.post('/')
#     assert response.status_code == 405
#     assert b'Method Not Allowed' in response.data
#     # Test inability to send a POST request to the alternate home page
#     response = testClient.post('/home')
#     assert response.status_code == 405
#     assert b'Method Not Allowed' in response.data
#
#
# def test_about(testClient):
#     """Test the about page."""
#     # Send a GET request to the application
#     response = testClient.get('/about')
#     assert response.status_code == 200
#     assert b'The Flask Blog is an established organization' in response.data
#     # Test inability to send a POST request to the about page
#     response = testClient.post('/about')
#     assert response.status_code == 405
#     assert b'Method Not Allowed' in response.data
