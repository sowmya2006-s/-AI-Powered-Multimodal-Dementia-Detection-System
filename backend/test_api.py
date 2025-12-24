import urllib.request
import json

# Test Signup
print("=== Testing Signup ===")
signup_data = json.dumps({"email": "apitest@example.com", "password": "StrongPass123"}).encode('utf-8')
signup_req = urllib.request.Request(
    'http://127.0.0.1:8000/api/accounts/signup/',
    data=signup_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(signup_req) as response:
        print(f"Status Code: {response.status}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"Error Status Code: {e.code}")
    print(f"Error Response: {e.read().decode('utf-8')}")

# Test Login
print("\n=== Testing Login ===")
login_data = json.dumps({"email": "apitest@example.com", "password": "StrongPass123"}).encode('utf-8')
login_req = urllib.request.Request(
    'http://127.0.0.1:8000/api/accounts/login/',
    data=login_data,
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(login_req) as response:
        print(f"Status Code: {response.status}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"Error Status Code: {e.code}")
    print(f"Error Response: {e.read().decode('utf-8')}")
