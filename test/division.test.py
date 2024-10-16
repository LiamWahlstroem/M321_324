import pytest
import jwt
import requests

SECRET_KEY = 'testSecret'

def generate_jwt(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

BASE_URL = "http://localhost:5000"

def test_valid_jwt_and_valid_numbers_divide():
    token = generate_jwt({'username': 'testuser'})
    response = requests.post(f'{BASE_URL}/divide',
                             json={'num1': 10, 'num2': 2},
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    data = response.json()
    assert data['result'] == 5  # 10 / 2 = 5

def test_invalid_jwt_divide():
    invalid_token = "invalid.jwt.token"
    response = requests.post(f'{BASE_URL}/divide',
                             json={'num1': 10, 'num2': 2},
                             headers={'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == 401
    data = response.json()
    assert data['error'] == 'Invalid Token'

def test_missing_jwt_divide():
    response = requests.post(f'{BASE_URL}/divide', json={'num1': 10, 'num2': 2})
    assert response.status_code == 401
    data = response.json()
    assert data['error'] == 'Authorization header missing'

def test_missing_numbers_divide():
    token = generate_jwt({'username': 'testuser'})
    response = requests.post(f'{BASE_URL}/divide',
                             json={'num1': 10},  # Missing num2
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Missing num2 in request body'

def test_non_numeric_input_divide():
    token = generate_jwt({'username': 'testuser'})
    response = requests.post(f'{BASE_URL}/divide',
                             json={'num1': 'abc', 'num2': 2},  # num1 is non-numeric
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Inputs must be numeric'

def test_division_by_zero():
    token = generate_jwt({'username': 'testuser'})
    response = requests.post(f'{BASE_URL}/divide',
                             json={'num1': 10, 'num2': 0},  # Division by zero
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Division by zero is undefined'
