#!/usr/bin/env python3
"""
API Testing Script for WhatsApp Flow API
Tests all endpoints of the application
"""

import requests
import json
from typing import Dict, Any

# Base URL - change this to your deployment URL or localhost
BASE_URL = "https://whatsapp-flow-virid.vercel.app"
# For local testing, use: BASE_URL = "http://localhost:5000"

def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_response(response: requests.Response):
    """Print formatted response"""
    print(f"\nStatus Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_health_check():
    """Test the health check endpoint"""
    print_section("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_debug():
    """Test the debug endpoint"""
    print_section("Debug Info")
    try:
        response = requests.get(f"{BASE_URL}/debug")
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_save_user():
    """Test the save-user endpoint"""
    print_section("Save User (POST /save-user)")
    
    # Test data
    test_data = {
        "user": "+1234567890",  # Phone number
        "parent_name": "John Doe",
        "child_name": "Jane Doe",
        "wishlist": ["toy1", "toy2"]
    }
    
    print(f"\nRequest Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/save-user",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_check_or_create_user():
    """Test the check-or-create-user endpoint"""
    print_section("Check or Create User (POST /check-or-create-user)")
    
    test_data = {
        "phone": "+1234567890"
    }
    
    print(f"\nRequest Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/check-or-create-user",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_all_users():
    """Test getting all users"""
    print_section("Get All Users (GET /users)")
    try:
        response = requests.get(f"{BASE_URL}/users")
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_user_by_phone():
    """Test getting a user by phone number"""
    print_section("Get User by Phone (GET /users/<phone>)")
    
    phone = "+1234567890"
    print(f"\nPhone: {phone}")
    
    try:
        response = requests.get(f"{BASE_URL}/users/{phone}")
        print_response(response)
        return response.status_code in [200, 404]
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_messages():
    """Test getting all messages"""
    print_section("Get All Messages (GET /messages)")
    try:
        response = requests.get(f"{BASE_URL}/messages")
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_message_by_id():
    """Test getting a message by ID"""
    print_section("Get Message by ID (GET /messages/<id>)")
    
    message_id = 1
    print(f"\nMessage ID: {message_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/messages/{message_id}")
        print_response(response)
        return response.status_code in [200, 404]
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_webhook_post():
    """Test the webhook POST endpoint"""
    print_section("Webhook POST (POST /webhook)")
    
    test_data = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "from": "+1234567890",
                        "text": {"body": "Test message"}
                    }]
                }
            }]
        }]
    }
    
    print(f"\nRequest Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_webhook_get():
    """Test the webhook GET endpoint (verification)"""
    print_section("Webhook GET Verification (GET /webhook)")
    
    params = {
        "hub.mode": "subscribe",
        "hub.verify_token": "your_verify_token_here",
        "hub.challenge": "test_challenge"
    }
    
    print(f"\nQuery Parameters: {json.dumps(params, indent=2)}")
    
    try:
        response = requests.get(f"{BASE_URL}/webhook", params=params)
        print_response(response)
        return response.status_code in [200, 403]
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  WhatsApp Flow API - Endpoint Testing")
    print("="*60)
    print(f"\nTesting endpoints at: {BASE_URL}")
    print("\nNote: Some tests may fail if the database is not set up properly.")
    
    results = {}
    
    # Run all tests
    results["Health Check"] = test_health_check()
    results["Debug"] = test_debug()
    results["Save User"] = test_save_user()
    results["Check or Create User"] = test_check_or_create_user()
    results["Get All Users"] = test_get_all_users()
    results["Get User by Phone"] = test_get_user_by_phone()
    results["Get All Messages"] = test_get_messages()
    results["Get Message by ID"] = test_get_message_by_id()
    results["Webhook POST"] = test_webhook_post()
    results["Webhook GET"] = test_webhook_get()
    
    # Print summary
    print_section("Test Summary")
    print("\n")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")

if __name__ == "__main__":
    main()

