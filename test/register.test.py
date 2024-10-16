import pytest
import requests

BASE_URL = "http://localhost:5000"  # Replace with your API URL

@pytest.mark.asyncio
async def test_successful_registration():
    # Test case: Successful registration
    username = "newuser"
    password = "newpassword"

    registration_response = requests.post(f'{BASE_URL}/register', json={
        'username': username,
        'password': password
    })
    
    assert registration_response.status_code == 200
    assert registration_response.json()['message'] == "User registered successfully"


@pytest.mark.asyncio
async def test_duplicate_registration():
    # Test case: Attempting to register an already registered username
    username = "testuser"  # Assuming this user already exists
    password = "testpassword"

    registration_response = requests.post(f'{BASE_URL}/register', json={
        'username': username,
        'password': password
    })

    assert registration_response.status_code == 400
    assert registration_response.json()['error'] == "User already exists"


@pytest.mark.asyncio
async def test_registration_with_missing_fields():
    # Test case: Registration with missing password
    username = "incompleteuser"

    registration_response = requests.post(f'{BASE_URL}/register', json={
        'username': username
        # No password provided
    })

    assert registration_response.status_code == 400
    assert registration_response.json()['error'] == "Missing required fields"


@pytest.mark.asyncio
async def test_registration_with_empty_fields():
    # Test case: Registration with empty username and password
    registration_response = requests.post(f'{BASE_URL}/register', json={
        'username': '',
        'password': ''
    })

    assert registration_response.status_code == 400
    assert registration_response.json()['error'] == "Username and password cannot be empty"
