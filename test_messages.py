#!/usr/bin/env python3
"""
Test messages page specifically
"""
import requests

session = requests.Session()

print("Testing messages page...")

# Login first
login_response = session.post("http://localhost:5000/login", 
                             data={'username': 'admin', 'password': 'admin123'})

print(f"Login status: {login_response.status_code}")

# Test messages page
print("\nTesting messages page...")
messages_response = session.get("http://localhost:5000/messages")
print(f"Messages status: {messages_response.status_code}")

if messages_response.status_code == 500:
    print("❌ Messages returned 500 error")
    print("Response content:")
    print(messages_response.text[:1000] + "..." if len(messages_response.text) > 1000 else messages_response.text)
elif messages_response.status_code == 200:
    print("✅ Messages page successful")
    print(f"Content length: {len(messages_response.text)} bytes")
elif messages_response.status_code == 302:
    print(f"Messages redirected to: {messages_response.headers.get('Location')}")
else:
    print(f"Unexpected status: {messages_response.status_code}")
