#!/usr/bin/env python3
"""
Simple test to manually login and access dashboard to see the exact error
"""
import requests

session = requests.Session()

print("Testing manual login...")

# Login
login_response = session.post("http://localhost:5000/login", 
                             data={'username': 'admin', 'password': 'admin123'})

print(f"Login status: {login_response.status_code}")
print(f"Login URL: {login_response.url}")

if login_response.status_code == 200:
    print("Login returned 200 - checking content...")
    if "Invalid" in login_response.text or "error" in login_response.text:
        print("❌ Login failed - credentials rejected")
    else:
        print("✅ Login page returned but no redirect")

# Try dashboard directly
print("\nTesting dashboard...")
dashboard_response = session.get("http://localhost:5000/dashboard")
print(f"Dashboard status: {dashboard_response.status_code}")

if dashboard_response.status_code == 500:
    print("❌ Dashboard returned 500 error")
    print("Response content:")
    print(dashboard_response.text[:1000] + "..." if len(dashboard_response.text) > 1000 else dashboard_response.text)
elif dashboard_response.status_code == 200:
    print("✅ Dashboard successful")
    print(f"Content length: {len(dashboard_response.text)} bytes")
elif dashboard_response.status_code == 302:
    print(f"Dashboard redirected to: {dashboard_response.headers.get('Location')}")
else:
    print(f"Unexpected status: {dashboard_response.status_code}")
