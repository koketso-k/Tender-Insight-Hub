#!/usr/bin/env python3
"""
SED Tender Insight Hub - System Test Script
Test the profile setup and scoring system
"""

import requests
import json
import time
import sys

# Configuration
API_BASE_URL = "http://localhost:5000/api"
TEST_USER = {
    "email": "test@example.com",
    "password": "testpassword123",
    "first_name": "Test",
    "last_name": "User",
    "company_name": "Test Construction Ltd"
}

def print_test_header(test_name):
    print(f"\n{'='*50}")
    print(f"Testing: {test_name}")
    print(f"{'='*50}")

def test_api_connection():
    """Test if API is running"""
    print_test_header("API Connection")
    try:
        response = requests.get(f"{API_BASE_URL}/cidb/categories", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and accessible")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("Make sure the backend server is running: python backend/app.py")
        return False

def test_user_registration():
    """Test user registration"""
    print_test_header("User Registration")
    try:
        response = requests.post(f"{API_BASE_URL}/auth/register", json=TEST_USER)
        if response.status_code == 201:
            print("✅ User registration successful")
            data = response.json()
            return data.get('token')
        elif response.status_code == 409:
            print("ℹ️ User already exists, attempting login...")
            return test_user_login()
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return None

def test_user_login():
    """Test user login"""
    print_test_header("User Login")
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        if response.status_code == 200:
            print("✅ User login successful")
            data = response.json()
            return data.get('token')
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_profile_creation(token):
    """Test profile creation and retrieval"""
    print_test_header("Profile Management")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Get initial profile
        response = requests.get(f"{API_BASE_URL}/profiles", headers=headers)
        if response.status_code == 200:
            print("✅ Profile retrieval successful")
            profile = response.json().get('profile', {})
            print(f"   Initial readiness score: {profile.get('readiness_score', 0)}")
            print(f"   Profile completion: {profile.get('profile_completion_percentage', 0)}%")
            return True
        else:
            print(f"❌ Profile retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Profile error: {e}")
        return False

def test_profile_update(token):
    """Test profile update with CIDB and BEE data"""
    print_test_header("Profile Update")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Sample profile data
    profile_data = {
        "cidb_grade": 5,
        "cidb_registration_number": "CIDB123456",
        "cidb_expiry_date": "2025-12-31",
        "cidb_work_categories": ["GB", "CE"],
        "bee_level": 2,
        "bee_certificate_number": "BEE789012",
        "bee_expiry_date": "2025-06-30",
        "bee_ownership_percentage": 51.0,
        "bee_management_control_percentage": 45.0,
        "bee_skills_development_percentage": 20.0,
        "bee_enterprise_development_percentage": 15.0,
        "bee_socio_economic_development_percentage": 10.0,
        "years_in_business": 10,
        "annual_turnover": 5000000.0,
        "number_of_employees": 25,
        "previous_tender_wins": 8,
        "previous_tender_applications": 12
    }
    
    try:
        response = requests.put(f"{API_BASE_URL}/profiles", 
                              json=profile_data, 
                              headers=headers)
        if response.status_code == 200:
            print("✅ Profile update successful")
            data = response.json()
            print(f"   New readiness score: {data['profile']['readiness_score']}")
            print(f"   Profile completion: {data['profile']['profile_completion_percentage']}%")
            return True
        else:
            print(f"❌ Profile update failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Profile update error: {e}")
        return False

def test_scoring_calculation(token):
    """Test score recalculation"""
    print_test_header("Score Recalculation")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.post(f"{API_BASE_URL}/profiles/score", headers=headers)
        if response.status_code == 200:
            print("✅ Score recalculation successful")
            data = response.json()
            print(f"   Readiness score: {data['readiness_score']}")
            print(f"   Profile completion: {data['profile_completion_percentage']}%")
            return True
        else:
            print(f"❌ Score recalculation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Score recalculation error: {e}")
        return False

def test_reference_data():
    """Test reference data endpoints"""
    print_test_header("Reference Data")
    
    try:
        # Test CIDB categories
        response = requests.get(f"{API_BASE_URL}/cidb/categories")
        if response.status_code == 200:
            categories = response.json().get('categories', [])
            print(f"✅ CIDB categories loaded: {len(categories)} categories")
        else:
            print(f"❌ CIDB categories failed: {response.status_code}")
            return False
        
        # Test scoring criteria
        response = requests.get(f"{API_BASE_URL}/scoring/criteria")
        if response.status_code == 200:
            criteria = response.json().get('criteria', [])
            print(f"✅ Scoring criteria loaded: {len(criteria)} criteria")
            return True
        else:
            print(f"❌ Scoring criteria failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Reference data error: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("SED Tender Insight Hub - System Test")
    print("=" * 50)
    
    # Test API connection
    if not test_api_connection():
        print("\n❌ Cannot proceed with tests - API not accessible")
        return False
    
    # Test user authentication
    token = test_user_registration()
    if not token:
        print("\n❌ Cannot proceed with tests - Authentication failed")
        return False
    
    # Test profile management
    if not test_profile_creation(token):
        print("\n❌ Profile creation test failed")
        return False
    
    # Test profile update
    if not test_profile_update(token):
        print("\n❌ Profile update test failed")
        return False
    
    # Test scoring
    if not test_scoring_calculation(token):
        print("\n❌ Scoring test failed")
        return False
    
    # Test reference data
    if not test_reference_data():
        print("\n❌ Reference data test failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed successfully!")
    print("The SED Tender Insight Hub is working correctly.")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

