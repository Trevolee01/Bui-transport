#!/usr/bin/env python
"""
Simple test script to check if the Django API is working
"""
import os
import sys
import django
import requests
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bui_transport.settings')
django.setup()

def test_server_connection():
    """Test if the server is running"""
    try:
        response = requests.get('http://127.0.0.1:8000/api/auth/register/', timeout=5)
        print(f"Server is running. Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the Django server with: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False

def test_registration():
    """Test user registration"""
    test_data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "phone_number": "1234567890",
        "role": "student",
        "password": "testpassword123",
        "password_confirm": "testpassword123"
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/api/auth/register/',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Registration Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return True
        else:
            print("❌ Registration failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing BUI Transport API...")
    print("=" * 50)
    
    if test_server_connection():
        print("\n📝 Testing Registration...")
        test_registration()
    
    print("\n" + "=" * 50)
    print("Test completed!")