#!/usr/bin/env python
"""
Simple API test script to verify endpoints are working
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    if response.status_code < 400:
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
    else:
        print(f"Error: {response.text}")

def test_api():
    print("🧪 Testing API Endpoints...")
    
    # 1. Login
    print("\n1️⃣  Testing Login...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    print_response("Login Response", response)
    
    if response.status_code == 200:
        token = response.json().get('access')
        headers = {'Authorization': f'Bearer {token}'}
        
        # 2. Get current user
        print("\n2️⃣  Testing Get Current User...")
        response = requests.get(f"{BASE_URL}/api/users/me/", headers=headers)
        print_response("Current User", response)
        
        # 3. List buildings
        print("\n3️⃣  Testing List Buildings...")
        response = requests.get(f"{BASE_URL}/api/buildings/", headers=headers)
        print_response("Buildings", response)
        
        # 4. List residents
        print("\n4️⃣  Testing List Residents...")
        response = requests.get(f"{BASE_URL}/api/residents/", headers=headers)
        print_response("Residents", response)
        
        # 5. List visitors
        print("\n5️⃣  Testing List Visitors...")
        response = requests.get(f"{BASE_URL}/api/visitors/", headers=headers)
        print_response("Visitors", response)
        
        # 6. List access points
        print("\n6️⃣  Testing List Access Points...")
        response = requests.get(f"{BASE_URL}/api/access/points/", headers=headers)
        print_response("Access Points", response)
        
        # 7. Get access logs stats
        print("\n7️⃣  Testing Access Logs Stats...")
        response = requests.get(f"{BASE_URL}/api/logs/stats/", headers=headers)
        print_response("Access Stats", response)
        
        print("\n✅ API Testing Complete!")
    else:
        print("\n❌ Login failed. Cannot test other endpoints.")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server. Make sure Django is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
