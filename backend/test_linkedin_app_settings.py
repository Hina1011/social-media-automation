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

async def test_linkedin_app_settings():
    """Test LinkedIn app settings and redirect URI configuration."""
    print("🔍 Testing LinkedIn App Settings...")
    
    # Test configuration
    print(f"Client ID: {settings.linkedin_client_id}")
    print(f"Client Secret: {settings.linkedin_client_secret}")
    print(f"Redirect URI: {settings.linkedin_redirect_uri}")
    print(f"Scope: {settings.linkedin_scope}")
    
    # Test the authorization URL
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={settings.linkedin_client_id}&redirect_uri={settings.linkedin_redirect_uri}&scope={settings.linkedin_scope}&state=test_state"
    
    print(f"\n🔗 Authorization URL:")
    print(f"{auth_url}")
    
    print(f"\n📋 IMPORTANT: You need to update your LinkedIn app settings!")
    print(f"1. Go to: https://www.linkedin.com/developers/apps")
    print(f"2. Click on your app (Client ID: {settings.linkedin_client_id})")
    print(f"3. Go to 'Auth' tab")
    print(f"4. Add this redirect URL: {settings.linkedin_redirect_uri}")
    print(f"5. Remove any old redirect URLs")
    print(f"6. Save changes")
    
    print(f"\n✅ Test completed!")
    print(f"📝 After updating LinkedIn app settings, try the OAuth flow again.")

if __name__ == "__main__":
    asyncio.run(test_linkedin_app_settings()) 