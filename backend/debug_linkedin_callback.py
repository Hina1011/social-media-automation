#!/usr/bin/env python3
"""
Debug LinkedIn callback endpoint
"""

import requests
import json

def test_linkedin_callback():
    """Test the LinkedIn callback endpoint."""
    print("🔧 Testing LinkedIn Callback Endpoint")
    print("=" * 50)
    
    # Test data that should match PlatformAuthRequest
    test_data = {
        "platform": "linkedin",
        "auth_code": "test_auth_code_123"
    }
    
    print(f"Test data: {json.dumps(test_data, indent=2)}")
    
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
            print("\n❌ 400 Bad Request - likely validation error")
            print("This suggests the request data format is incorrect")
        elif response.status_code == 401:
            print("\n❌ 401 Unauthorized - authentication required")
            print("This is expected without a valid token")
        else:
            print(f"\n✅ Unexpected status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the server is running on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_expected_format():
    """Show the expected request format."""
    print("\n📝 Expected Request Format:")
    print("=" * 50)
    print("POST /api/platforms/linkedin/callback")
    print("Headers:")
    print("  Content-Type: application/json")
    print("  Authorization: Bearer <your_jwt_token>")
    print("\nBody:")
    print("  {")
    print('    "platform": "linkedin",')
    print('    "auth_code": "<authorization_code_from_linkedin>"')
    print("  }")
    
    print("\n📝 PlatformAuthRequest Model:")
    print("=" * 50)
    print("class PlatformAuthRequest(BaseModel):")
    print('    platform: Literal["instagram", "linkedin", "facebook", "twitter"]')
    print("    auth_code: Optional[str] = None")
    print("    username: Optional[str] = None")
    print("    password: Optional[str] = None")

def main():
    """Main function."""
    print("LinkedIn Callback Debug Tool")
    print("=" * 50)
    
    test_linkedin_callback()
    show_expected_format()

if __name__ == "__main__":
    main() 