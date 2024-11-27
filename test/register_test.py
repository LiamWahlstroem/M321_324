import pytest
import requests

BASE_URL = "http://localhost:8001"  # Updated to match the host port mapping

@pytest.mark.asyncio
async def test_successful_registration():
    # Test case: Successful registration
    username = "newuser"
    password = "newpassword"

    registration_response = requests.post(f'{BASE_URL}/register', json={
        'username': username,
        'password': password
    })
    
    assert registration_response.status_code == 400 #todo mit liam abklären



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



@pytest.mark.asyncio
async def test_registration_with_missing_fields():
    # Test case: Registration with missing password
    username = "incompleteuser"

    registration_response = requests.post(f'{BASE_URL}/register', json={
        'username': username
        # No password provided
    })

    assert registration_response.status_code == 422



@pytest.mark.asyncio
async def test_registration_with_empty_fields():
    # Test case: Registration with empty username and password
    registration_response = requests.post(f'{BASE_URL}/register', json={
        'username': '',
        'password': ''
    })

    assert registration_response.status_code == 400
