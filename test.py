"""
Test script for User Preferences Microservice
Run this to verify all endpoints are working correctly
"""

import requests
import json
from time import time

BASE_URL = "http://localhost:5003"
TEST_USER_ID = 999  # Test user ID

def test_health_check():
    """Test health check endpoint"""
    print("\nTesting Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("Health check passed")

def test_get_options():
    """Test getting available options"""
    print("\nTesting Get Options...")
    response = requests.get(f"{BASE_URL}/preferences/options")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("Get options passed")

def test_get_preferences_default():
    """Test getting preferences when none exist (should return defaults)"""
    print("\nTesting Get Preferences (Default)...")
    response = requests.get(f"{BASE_URL}/preferences/{TEST_USER_ID}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    print("Get default preferences passed")

def test_save_preferences():
    """Test saving new preferences"""
    print("\nTesting Save Preferences...")
    preferences = {
        "language": "Korean",
        "email_notification": False,
        "theme": "spring-summer",
        "font_size": "large"
    }
    
    start_time = time()
    response = requests.post(
        f"{BASE_URL}/preferences/{TEST_USER_ID}",
        json=preferences
    )
    elapsed = (time() - start_time) * 1000  # Convert to milliseconds
    
    print(f"Status: {response.status_code}")
    print(f"Response time: {elapsed:.2f}ms")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert data['preferences']['language'] == "Korean"
    assert data['preferences']['email_notification'] == False
    assert data['preferences']['theme'] == "spring-summer"
    assert data['preferences']['font_size'] == "large"
    
    # Check performance requirement (500ms)
    if elapsed < 500:
        print(f"Performance requirement met: {elapsed:.2f}ms < 500ms")
    else:
        print(f"Performance warning: {elapsed:.2f}ms >= 500ms")
    
    print("Save preferences passed")

def test_update_preferences():
    """Test updating existing preferences"""
    print("\nTesting Update Preferences...")
    preferences = {
        "language": "English",
        "font_size": "medium"
    }
    
    response = requests.put(
        f"{BASE_URL}/preferences/{TEST_USER_ID}",
        json=preferences
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert data['preferences']['language'] == "English"
    assert data['preferences']['font_size'] == "medium"
    print("Update preferences passed")

def test_get_preferences_saved():
    """Test getting saved preferences"""
    print("\nTesting Get Saved Preferences...")
    
    start_time = time()
    response = requests.get(f"{BASE_URL}/preferences/{TEST_USER_ID}")
    elapsed = (time() - start_time) * 1000
    
    print(f"Status: {response.status_code}")
    print(f"Response time: {elapsed:.2f}ms")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert 'preferences' in data
    
    # Check performance requirement
    if elapsed < 500:
        print(f"Performance requirement met: {elapsed:.2f}ms < 500ms")
    else:
        print(f"Performance warning: {elapsed:.2f}ms >= 500ms")
    
    print("Get saved preferences passed")

def test_invalid_preferences():
    """Test validation with invalid preferences"""
    print("\nTesting Invalid Preferences Validation...")
    invalid_preferences = {
        "language": "Spanish",  # Invalid
        "theme": "rainbow",     # Invalid
        "font_size": "huge"     # Invalid
    }
    
    response = requests.post(
        f"{BASE_URL}/preferences/{TEST_USER_ID}",
        json=invalid_preferences
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 400
    data = response.json()
    assert data['success'] == False
    assert 'errors' in data
    print("Validation test passed")

def test_reset_preferences():
    """Test resetting preferences to defaults"""
    print("\nTesting Reset Preferences...")
    response = requests.post(f"{BASE_URL}/preferences/{TEST_USER_ID}/reset")
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    assert data['preferences']['language'] == "English"
    assert data['preferences']['email_notification'] == True
    assert data['preferences']['theme'] == "winter"
    assert data['preferences']['font_size'] == "medium"
    print("Reset preferences passed")

def test_delete_preferences():
    """Test deleting preferences"""
    print("\nTesting Delete Preferences...")
    response = requests.delete(f"{BASE_URL}/preferences/{TEST_USER_ID}")
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    assert data['success'] == True
    print("Delete preferences passed")

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Starting User Preferences Microservice Tests")
    print("="*60)
    
    try:
        test_health_check()
        test_get_options()
        test_get_preferences_default()
        test_save_preferences()
        test_update_preferences()
        test_get_preferences_saved()
        test_invalid_preferences()
        test_reset_preferences()
        test_delete_preferences()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
    except requests.exceptions.ConnectionError:
        print("\nERROR: Cannot connect to service. Make sure it's running on http://localhost:5003")
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")

if __name__ == "__main__":
    run_all_tests()