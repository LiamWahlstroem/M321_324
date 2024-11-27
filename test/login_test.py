import pytest
import requests
import jwt

BASE_URL = "http://localhost:8000"  # Updated to match the host port mapping
SECRET_KEY = 'testSecret'  # Adjust this as necessary

@pytest.mark.asyncio
async def test_successful_login():
    # Test case: Successful login
    username = "testuser"  # This user should already be registered
    password = "testpassword"

    login_response = requests.post(f'{BASE_URL}/login', json={
        'username': username,
        'password': password
    })
    
    assert login_response.status_code == 200
    token = login_response.json()['message']

    # Decode and verify the JWT token
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    assert decoded_payload['username'] == username

@pytest.mark.asyncio
async def test_login_with_invalid_password():
    # Test case: Login with an invalid password
    username = "testuser"
    invalid_password = "wrongpassword"

    login_response = requests.post(f'{BASE_URL}/login', json={
        'username': username,
        'password': invalid_password
    })

    assert login_response.status_code == 400

@pytest.mark.asyncio
async def test_login_with_non_existent_user():
    # Test case: Login with a non-existent user
    non_existent_username = "nonexistentuser"
    password = "password"

    login_response = requests.post(f'{BASE_URL}/login', json={
        'username': non_existent_username,
        'password': password
    })

    assert login_response.status_code == 404

@pytest.mark.asyncio
async def test_login_with_missing_fields():
    # Test case: Login with missing password
    username = "testuser"

    login_response = requests.post(f'{BASE_URL}/login', json={
        'username': username
        # No password provided
    })

    assert login_response.status_code == 422

@pytest.mark.asyncio
async def test_login_with_empty_fields():
    # Test case: Login with empty username and password
    login_response = requests.post(f'{BASE_URL}/login', json={
        'username': '',
        'password': ''
    })

    assert login_response.status_code == 200
