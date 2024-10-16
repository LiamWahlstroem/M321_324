import pytest
import jwt
import requests

SECRET_KEY = 'testSecret'

# Helper function to create a JWT
def generate_jwt(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

BASE_URL = "http://localhost:5000"

def test_valid_jwt_and_valid_numbers_add():
    # Test case 1: Valid JWT and valid numbers
    token = generate_jwt({'username': 'testuser'})  # Generate a valid JWT
    response = requests.post(f'{BASE_URL}/add', 
                             json={'num1': 5, 'num2': 10}, 
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.json()
    assert data['result'] == 15  # 5 + 10 = 15

def test_invalid_jwt_add():
    # Test case 2: Invalid JWT
    invalid_token = "invalid.jwt.token"  # Malformed or invalid token
    response = requests.post(f'{BASE_URL}/add', 
                             json={'num1': 5, 'num2': 10}, 
                             headers={'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == 401
    data = response.json()
    assert data['error'] == 'Invalid Token'

def test_missing_jwt_add():
    # Test case 3: Missing JWT
    response = requests.post(f'{BASE_URL}/add', json={'num1': 5, 'num2': 10})
    assert response.status_code == 401
    data = response.json()
    assert data['error'] == 'Authorization header missing'

def test_missing_numbers_add():
    # Test case 4: Missing numbers in request body
    token = generate_jwt({'username': 'testuser'})  # Generate a valid JWT
    response = requests.post(f'{BASE_URL}/add', 
                             json={'num1': 5},  # Only one number is provided
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Missing num2 in request body'

def test_non_numeric_input_add():
    # Test case 5: Non-numeric input
    token = generate_jwt({'username': 'testuser'})  # Generate a valid JWT
    response = requests.post(f'{BASE_URL}/add', 
                             json={'num1': 'abc', 'num2': 10},  # 'num1' is not a number
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Inputs must be numeric'
