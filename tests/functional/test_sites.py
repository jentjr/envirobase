"""
This file (test_sites.py contains the functional tests for the sites blueprint
"""

def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Welcome to Envirobase" in response.data
