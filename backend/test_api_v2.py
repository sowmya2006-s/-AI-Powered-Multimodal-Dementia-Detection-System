import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_signup():
    url = f"{BASE_URL}/api/accounts/signup/"
    data = {
        "email": "testuser_v2@example.com",
        "password": "testpassword123"
    }
    print(f"Testing Signup: {url}")
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code in [201, 400] # 400 if user exists
    except Exception as e:
        print(f"Signup error: {e}")
        return False

def test_login():
    url = f"{BASE_URL}/api/accounts/login/"
    data = {
        "email": "testuser_v2@example.com",
        "password": "testpassword123"
    }
    print(f"\nTesting Login: {url}")
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            tokens = response.json()
            print("Login successful.")
            return tokens.get("access")
        else:
            print(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def test_create_patient(access_token):
    url = f"{BASE_URL}/api/patients/create/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "name":"John Doe",
        "age":65,
        "gender":"Male",
        "language":"English",
        "education":"Graduate",
        "medical_history":"Diabetes"
    }
    print(f"\nTesting Patient Create: {url}")
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 201
    except Exception as e:
        print(f"Patient create error: {e}")
        return False

if __name__ == "__main__":
    if test_signup() or True: # Try login even if signup fails (user might exist)
        token = test_login()
        if token:
            test_create_patient(token)
        else:
            print("Skipping patient creation due to login failure.")
