import asyncio
import sys
import os
import requests
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_linkedin_token_exchange():
    """Test LinkedIn token exchange with detailed logging."""
    print("🔍 Testing LinkedIn Token Exchange...")
    
    # Test configuration
    print(f"Client ID: {settings.linkedin_client_id}")
    print(f"Client Secret: {settings.linkedin_client_secret}")
    print(f"Redirect URI: {settings.linkedin_redirect_uri}")
    print(f"Scope: {settings.linkedin_scope}")
    
    # Test the token exchange URL
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    print(f"\n🔗 Token URL: {token_url}")
    
    # Test with a dummy code (this will fail, but we can see the error)
    test_data = {
        "grant_type": "authorization_code",
        "code": "test_code_123",
        "client_id": settings.linkedin_client_id,
        "client_secret": settings.linkedin_client_secret,
        "redirect_uri": settings.linkedin_redirect_uri
    }
    
    print(f"\n📤 Test request data:")
    for key, value in test_data.items():
        if key != "client_secret":
            print(f"  {key}: {value}")
        else:
            print(f"  {key}: {'*' * len(value)}")
    
    try:
        response = requests.post(token_url, data=test_data)
        print(f"\n📥 Response Status: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        print(f"📥 Response Body: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n✅ Debug test completed!")
    print("📝 Next steps:")
    print("1. Update LinkedIn app redirect URI to: http://localhost:3000/linkedin-callback")
    print("2. Try the OAuth flow again")
    print("3. Check the actual authorization code in the logs")

if __name__ == "__main__":
    asyncio.run(test_linkedin_token_exchange()) 