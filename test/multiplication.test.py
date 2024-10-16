import pytest
import jwt
import requests

SECRET_KEY = 'testSecret'

def generate_jwt(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

BASE_URL = "http://localhost:5000"

def test_valid_jwt_and_valid_numbers_multiply():
    token = generate_jwt({'username': 'testuser'})
    response = requests.post(f'{BASE_URL}/multiply',
                             json={'num1': 5, 'num2': 10},
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.json()
    assert data['result'] == 50  # 5 * 10 = 50

def test_invalid_jwt_multiply():
    invalid_token = "invalid.jwt.token"
    response = requests.post(f'{BASE_URL}/multiply',
                             json={'num1': 5, 'num2': 10},
                             headers={'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == 401
    data = response.json()
    assert data['error'] == 'Invalid Token'

def test_missing_jwt_multiply():
    response = requests.post(f'{BASE_URL}/multiply', json={'num1': 5, 'num2': 10})
    assert response.status_code == 401
    data = response.json()
    assert data['error'] == 'Authorization header missing'

def test_missing_numbers_multiply():
    token = generate_jwt({'username': 'testuser'})
    response = requests.post(f'{BASE_URL}/multiply',
                             json={'num1': 5},  # Missing num2
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Missing num2 in request body'

def test_non_numeric_input_multiply():
    token = generate_jwt({'username': 'testuser'})
    response = requests.post(f'{BASE_URL}/multiply',
                             json={'num1': 'abc', 'num2': 10},  # num1 is non-numeric
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Inputs must be numeric'
