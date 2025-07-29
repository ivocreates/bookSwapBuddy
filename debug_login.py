import requests

def debug_login():
    base_url = "http://localhost:5000"
    
    # Test login
    session = requests.Session()
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"Login Response Status: {response.status_code}")
        print(f"Login Response Headers: {dict(response.headers)}")
        print(f"Login Response URL: {response.url}")
        
        if 'Location' in response.headers:
            redirect_url = response.headers['Location']
            print(f"Redirect Location: {redirect_url}")
            
            # Build full URL if it's relative
            if redirect_url.startswith('/'):
                redirect_url = f"{base_url}{redirect_url}"
            
            # Follow the redirect
            redirect_response = session.get(redirect_url)
            print(f"Redirect Response Status: {redirect_response.status_code}")
            print(f"Redirect Response URL: {redirect_response.url}")
        
        # Try accessing dashboard directly
        dashboard_response = session.get(f"{base_url}/dashboard")
        print(f"Dashboard Response Status: {dashboard_response.status_code}")
        print(f"Dashboard Response URL: {dashboard_response.url}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_login()
