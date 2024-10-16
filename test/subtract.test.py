import pytest
import jwt
import requests

SECRET_KEY = 'testSecret'

# Helper function to create a JWT
def generate_jwt(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

BASE_URL = "http://localhost:5000"

def test_valid_jwt_and_valid_numbers_subtract():
    token = generate_jwt({'username': 'testuser'})
    response = requests.post(f'{BASE_URL}/subtract',
                             json={'num1': 10, 'num2': 5},
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.json()
    assert data['result'] == 5  # 10 - 5 = 5

def test_invalid_jwt_subtract():
    invalid_token = "invalid.jwt.token"
    response = requests.post(f'{BASE_URL}/subtract',
                             json={'num1': 10, 'num2': 5},
                             headers={'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == 401
    data = response.json()
    assert data['error'] == 'Invalid Token'

def test_missing_jwt_subtract():
    response = requests.post(f'{BASE_URL}/subtract', json={'num1': 10, 'num2': 5})
    assert response.status_code == 401
    data = response.json()
    assert data['error'] == 'Authorization header missing'

def test_missing_numbers_subtract():
    token = generate_jwt({'username': 'testuser'})
    response = requests.post(f'{BASE_URL}/subtract',
                             json={'num1': 10},  # Missing num2
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Missing num2 in request body'

def test_non_numeric_input_subtract():
    token = generate_jwt({'username': 'testuser'})
    response = requests.post(f'{BASE_URL}/subtract',
                             json={'num1': 'abc', 'num2': 5},  # num1 is non-numeric
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Inputs must be numeric'
