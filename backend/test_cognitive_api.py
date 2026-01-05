import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/cognitive/"
PATIENT_ID = 1

def test_cognitive_flow():
    session = requests.Session()
    
    # 1. Start Test
    print("--- Starting Test ---")
    response = session.post(f"{BASE_URL}start/", json={"patient_id": PATIENT_ID, "test_mode": "visual"})
    print(response.status_code, response.json())
    assert response.status_code == 200
    
    # 2. Run 4 rounds
    for i in range(4):
        print(f"\n--- Round {i+1} ---")
        # Generate Round
        response = session.get(f"{BASE_URL}generate-round/")
        print("Generate:", response.status_code, response.json())
        assert response.status_code == 200
        round_data = response.json()
        target = round_data["target"]
        
        # Submit Answer (always correct for this test)
        response = session.post(f"{BASE_URL}submit-answer/", json={"answer": target})
        print("Submit:", response.status_code, response.json())
        assert response.status_code == 200
        
    # 3. Finish Test
    print("\n--- Finishing Test ---")
    response = session.post(f"{BASE_URL}finish/")
    print(response.status_code, response.json())
    assert response.status_code == 201
    
    print("\nVerification Successful!")

if __name__ == "__main__":
    try:
        test_cognitive_flow()
    except Exception as e:
        print(f"Test Failed: {e}")
