#!/usr/bin/env python3
"""
Simple LinkedIn callback test
"""

import requests
import json

def test_linkedin_callback_with_real_data():
    """Test the LinkedIn callback with real data from browser."""
    print("🔧 LinkedIn Callback Test")
    print("=" * 50)
    
    print("📝 Instructions:")
    print("1. Go to your frontend and try LinkedIn Connect")
    print("2. When you get the 400 error, check the browser console")
    print("3. Look for the request details in the Network tab")
    print("4. Copy the auth_code from the request body")
    print("5. Enter it below when prompted")
    
    auth_code = input("\nEnter the auth_code from the browser request: ").strip()
    
    if not auth_code:
        print("❌ No auth code provided")
        return
    
    # Test data
    test_data = {
        "platform": "linkedin",
        "auth_code": auth_code
    }
    
    print(f"\n🧪 Testing with auth code: {auth_code[:20]}...")
    
    try:
        # Test the callback endpoint
        response = requests.post(
            "http://localhost:8000/api/platforms/linkedin/callback",
            json=test_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer test_token"  # This will fail auth, but we'll see the validation error
            }
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("\n❌ 400 Bad Request")
            print("This suggests the auth code is invalid or expired")
            print("Try getting a fresh auth code by clicking LinkedIn Connect again")
        elif response.status_code == 401:
            print("\n❌ 401 Unauthorized - authentication required")
            print("This is expected without a valid token")
        else:
            print(f"\n✅ Unexpected status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_debug_steps():
    """Show debug steps."""
    print("\n📝 Debug Steps:")
    print("=" * 50)
    print("1. 🔍 Check Browser Console:")
    print("   - Open Developer Tools (F12)")
    print("   - Go to Network tab")
    print("   - Try LinkedIn Connect")
    print("   - Look for the failed request")
    print("   - Check the request body and response")
    
    print("\n2. 🔍 Check Backend Logs:")
    print("   - Look at your backend server console")
    print("   - Look for LinkedIn API errors")
    print("   - Look for token exchange errors")
    
    print("\n3. 🔄 Try Again:")
    print("   - Clear browser cache")
    print("   - Log out and log back in")
    print("   - Try LinkedIn Connect again")

def main():
    """Main function."""
    print("LinkedIn Callback Debug Tool")
    print("=" * 50)
    
    test_linkedin_callback_with_real_data()
    show_debug_steps()

if __name__ == "__main__":
    main() 