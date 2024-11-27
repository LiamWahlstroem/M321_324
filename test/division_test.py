import pytest
import jwt
import requests

SECRET_KEY = 'testSecret'

def createJWT(username):
    payload = {
        'username': username
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

BASE_URL = "http://localhost:8006"  # Updated to match the host port mapping

def test_valid_jwt_and_valid_numbers_divide():
    # Test case 1: Valid JWT and valid numbers
    token = createJWT('testuser')  # Generate a valid JWT
    response = requests.post(f'{BASE_URL}/division', 
                             json={'num1': 10, 'num2': 2, 'jwt': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyIn0.tVEz8RR5BzDySr_hPLaLle5bzSc04gvq_HE5-dUKlho"}) 
    assert response.status_code == 200
    data = response.json()
    assert data['result'] == 5  # 10 / 2 = 5

def test_invalid_jwt_divide():
    # Test case 2: Invalid JWT
    invalid_token = "invalid.jwt.token"  # Malformed or invalid token
    response = requests.post(f'{BASE_URL}/division', 
                             json={'num1': 10, 'num2': 2, 'jwt': invalid_token})
    assert response.status_code == 401

def test_missing_jwt_divide():
    # Test case 3: Missing JWT
    response = requests.post(f'{BASE_URL}/division', json={'num1': 10, 'num2': 2})
    assert response.status_code == 422

def test_missing_numbers_divide():
    # Test case 4: Missing numbers in request body
    token = createJWT('testuser')  # Generate a valid JWT
    response = requests.post(f'{BASE_URL}/division', 
                             json={'num1': 10, 'jwt': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyIn0.tVEz8RR5BzDySr_hPLaLle5bzSc04gvq_HE5-dUKlho"})  # Only one number is provided
    assert response.status_code == 422

def test_non_numeric_input_divide():
    # Test case 5: Non-numeric input
    token = createJWT('testuser')  # Generate a valid JWT
    response = requests.post(f'{BASE_URL}/division', 
                             json={'num1': 'abc', 'num2': 2, 'jwt': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyIn0.tVEz8RR5BzDySr_hPLaLle5bzSc04gvq_HE5-dUKlho"})  # 'num1' is not a number
    assert response.status_code == 422
