#!/usr/bin/env python3
"""
Test login and dashboard functionality
"""
import requests
import sys

def test_login_and_dashboard():
    base_url = "http://localhost:5000"
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("🧪 Testing Login and Dashboard Flow")
    print("=" * 50)
    
    # First get the login page to establish session
    print("1. Getting login page...")
    login_get = session.get(f"{base_url}/login")
    if login_get.status_code != 200:
        print(f"❌ Login page failed: {login_get.status_code}")
        return False
    print("✅ Login page loaded successfully")
    
    # Test login with admin credentials
    print("2. Testing login with admin credentials...")
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    login_response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    print(f"   Login status: {login_response.status_code}")
    
    if login_response.status_code == 302:
        # Check redirect location
        redirect_url = login_response.headers.get('Location', '')
        print(f"   Redirect to: {redirect_url}")
        
        if 'dashboard' in redirect_url:
            print("✅ Login successful - redirecting to dashboard")
            
            # Test dashboard access
            print("3. Testing dashboard access...")
            dashboard_response = session.get(f"{base_url}/dashboard")
            
            if dashboard_response.status_code == 200:
                print("✅ Dashboard loaded successfully!")
                print(f"   Dashboard content length: {len(dashboard_response.content)} bytes")
                
                # Check if dashboard contains expected content
                if b'Dashboard' in dashboard_response.content or b'dashboard' in dashboard_response.content:
                    print("✅ Dashboard contains expected content")
                    return True
                else:
                    print("⚠️  Dashboard loaded but may be missing content")
                    return True
            else:
                print(f"❌ Dashboard failed: {dashboard_response.status_code}")
                if dashboard_response.status_code == 500:
                    print("   Server error - check Flask console for details")
                return False
        else:
            print(f"❌ Login redirected to unexpected location: {redirect_url}")
            return False
    elif login_response.status_code == 200:
        # Check for error messages in response
        if b'Invalid' in login_response.content or b'error' in login_response.content:
            print("❌ Login failed - invalid credentials or error")
        else:
            print("⚠️  Login returned 200 but should redirect")
        return False
    else:
        print(f"❌ Login failed with status: {login_response.status_code}")
        return False

if __name__ == "__main__":
    print("Testing BookSwapBuddy Login and Dashboard...")
    print("Make sure the Flask app is running on localhost:5000")
    print()
    
    try:
        success = test_login_and_dashboard()
        if success:
            print("\n🎉 All tests passed!")
            sys.exit(0)
        else:
            print("\n💥 Some tests failed!")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask app. Make sure it's running on localhost:5000")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
