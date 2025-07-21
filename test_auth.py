#!/usr/bin/env python
"""
Test script to verify authentication system returns staff information
"""
import requests
import json

# Test configuration
BASE_URL = 'http://localhost:8000'
LOGIN_URL = f'{BASE_URL}/api/auth/login/'
DASHBOARD_URL = f'{BASE_URL}/appointments/api/staff/dashboard/'
USER_INFO_URL = f'{BASE_URL}/api/auth/user-info/'

# Test credentials
TEST_USERNAME = 'nurse_test'
TEST_PASSWORD = 'testpass123'

def test_login():
    """Test login endpoint returns staff information"""
    print("Testing Login Endpoint...")
    print(f"URL: {LOGIN_URL}")
    
    login_data = {
        'username': TEST_USERNAME,
        'password': TEST_PASSWORD
    }
    
    try:
        response = requests.post(LOGIN_URL, json=login_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful!")
            print(f"Token: {data.get('token', 'Not found')}")
            print(f"User ID: {data.get('user_id', 'Not found')}")
            print(f"Username: {data.get('username', 'Not found')}")
            
            if 'staff' in data:
                staff = data['staff']
                print("✅ Staff information found:")
                print(f"  Staff ID: {staff.get('id', 'Not found')}")
                print(f"  Name: {staff.get('first_name', '')} {staff.get('last_name', '')}")
                print(f"  Role: {staff.get('role_display', 'Not found')}")
                print(f"  Email: {staff.get('email', 'Not found')}")
                print(f"  Active: {staff.get('is_active', 'Not found')}")
            else:
                print("❌ No staff information found")
            
            return data.get('token')
        else:
            print(f"❌ Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_user_info(token):
    """Test user info endpoint returns staff information"""
    print("\nTesting User Info Endpoint...")
    print(f"URL: {USER_INFO_URL}")
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(USER_INFO_URL, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ User info retrieved successfully!")
            print(f"User ID: {data.get('user_id', 'Not found')}")
            print(f"Username: {data.get('username', 'Not found')}")
            
            if 'staff' in data:
                staff = data['staff']
                print("✅ Staff information found:")
                print(f"  Staff ID: {staff.get('id', 'Not found')}")
                print(f"  Name: {staff.get('first_name', '')} {staff.get('last_name', '')}")
                print(f"  Role: {staff.get('role_display', 'Not found')}")
                print(f"  Email: {staff.get('email', 'Not found')}")
                print(f"  Active: {staff.get('is_active', 'Not found')}")
            else:
                print("❌ No staff information found")
        else:
            print(f"❌ User info failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_dashboard(token):
    """Test dashboard endpoint returns staff information"""
    print("\nTesting Dashboard Endpoint...")
    print(f"URL: {DASHBOARD_URL}")
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(DASHBOARD_URL, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Dashboard retrieved successfully!")
            
            if 'staff' in data:
                staff = data['staff']
                print("✅ Staff information found in dashboard:")
                print(f"  Staff ID: {staff.get('id', 'Not found')}")
                print(f"  Name: {staff.get('first_name', '')} {staff.get('last_name', '')}")
                print(f"  Role: {staff.get('role_display', 'Not found')}")
                print(f"  Email: {staff.get('email', 'Not found')}")
                print(f"  Active: {staff.get('is_active', 'Not found')}")
            else:
                print("❌ No staff information found in dashboard")
            
            # Show stats
            if 'stats' in data:
                stats = data['stats']
                print(f"Dashboard Stats:")
                print(f"  Today's appointments: {stats.get('today_count', 0)}")
                print(f"  In progress: {stats.get('in_progress_count', 0)}")
                print(f"  Upcoming: {stats.get('upcoming_count', 0)}")
                print(f"  Recent incidents: {stats.get('recent_incidents_count', 0)}")
                print(f"  Recent seizures: {stats.get('recent_seizures_count', 0)}")
        else:
            print(f"❌ Dashboard failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing Authentication System with Staff Information")
    print("=" * 60)
    
    # Test login
    token = test_login()
    
    if token:
        # Test user info
        test_user_info(token)
        
        # Test dashboard
        test_dashboard(token)
    else:
        print("❌ Cannot proceed with other tests without valid token")
    
    print("\n" + "=" * 60)
    print("🏁 Testing completed!")

if __name__ == '__main__':
    main() 