import requests
import time

def test_routes():
    base_url = "http://localhost:5000"
    
    # Public routes that should work without login
    public_routes = [
        "/",
        "/register", 
        "/login",
        "/books",
        "/leaderboard",
        "/health"
    ]
    
    print("Testing public routes...")
    for route in public_routes:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
            print(f"{route}: {status}")
        except Exception as e:
            print(f"{route}: ❌ ERROR - {e}")
    
    print("\nTesting login...")
    # Test login
    session = requests.Session()
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = session.post(f"{base_url}/login", data=login_data, timeout=5)
        if response.status_code == 200 and "dashboard" in response.url:
            print("Login: ✅ PASS")
            
            # Test protected routes
            protected_routes = [
                "/dashboard",
                "/add_book",
                "/messages", 
                "/wishlist",
                "/profile",
                "/analytics"
            ]
            
            print("\nTesting protected routes...")
            for route in protected_routes:
                try:
                    response = session.get(f"{base_url}{route}", timeout=5)
                    status = "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})"
                    print(f"{route}: {status}")
                except Exception as e:
                    print(f"{route}: ❌ ERROR - {e}")
        else:
            print("Login: ❌ FAIL")
    except Exception as e:
        print(f"Login: ❌ ERROR - {e}")

if __name__ == "__main__":
    print("🧪 Testing BookSwapBuddy Routes\n")
    print("Make sure the Flask app is running on localhost:5000")
    print("-" * 50)
    test_routes()
    print("-" * 50)
    print("✅ Route testing completed!")
