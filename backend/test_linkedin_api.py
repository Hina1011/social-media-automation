#!/usr/bin/env python3
"""
Simple LinkedIn API test
"""

import requests
import json

def test_linkedin_auth_url():
    """Test LinkedIn auth URL generation."""
    print("🔧 Testing LinkedIn Auth URL")
    print("=" * 40)
    
    try:
        # Test the auth URL endpoint
        response = requests.get("http://localhost:8000/api/platforms/linkedin/auth-url")
        
        if response.status_code == 200:
            data = response.json()
            auth_url = data.get("auth_url")
            if auth_url and "linkedin.com/oauth/v2/authorization" in auth_url:
                print("✅ LinkedIn auth URL generated successfully")
                print(f"   URL: {auth_url[:100]}...")
                return True
            else:
                print("❌ Invalid auth URL format")
                return False
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_server_status():
    """Test if the server is running."""
    print("\n🔧 Testing Server Status")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Server is running on port 8000")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running on port 8000")
        print("   Start the server with: python start_server.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function."""
    print("LinkedIn API Integration Test")
    print("=" * 50)
    
    # First test if server is running
    if not test_server_status():
        print("\n💡 To start the server, run:")
        print("   python start_server.py")
        return
    
    # Test LinkedIn auth URL
    test_linkedin_auth_url()
    
    print("\n" + "=" * 50)
    print("✅ LinkedIn integration test completed!")
    print("\n💡 Next steps:")
    print("   1. Open http://localhost:3000 in your browser")
    print("   2. Go to the Platforms page")
    print("   3. Click 'LinkedIn Connect' - it should work now!")

if __name__ == "__main__":
    main() 