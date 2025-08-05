import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.linkedin_service import LinkedInService
from config import settings

async def test_linkedin_config():
    """Test LinkedIn configuration and token exchange."""
    print("🔍 Testing LinkedIn Configuration...")
    print(f"Client ID: {settings.linkedin_client_id}")
    print(f"Client Secret: {settings.linkedin_client_secret}")
    print(f"Redirect URI: {settings.linkedin_redirect_uri}")
    print(f"Scope: {settings.linkedin_scope}")
    
    linkedin_service = LinkedInService()
    
    # Test auth URL generation
    auth_url = linkedin_service.get_auth_url("test_state")
    print(f"\n🔗 Auth URL: {auth_url}")
    
    print("\n✅ Configuration test completed!")
    print("📝 Next steps:")
    print("1. Update LinkedIn app redirect URI to: http://localhost:3000/linkedin-callback")
    print("2. Try the OAuth flow again")
    print("3. Check backend logs for detailed error messages")

if __name__ == "__main__":
    asyncio.run(test_linkedin_config()) 