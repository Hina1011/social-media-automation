#!/usr/bin/env python3
"""
LinkedIn Configuration Test Script
This script helps verify your LinkedIn OAuth configuration and diagnose issues.
"""

import os
import sys
from urllib.parse import urlencode

def check_env_file():
    """Check if .env file exists and has LinkedIn credentials."""
    print("🔍 Checking .env file...")
    
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_file):
        print("❌ .env file not found!")
        print("   Please create a .env file in the backend directory.")
        return False
    
    print("✅ .env file found")
    
    # Read and check LinkedIn credentials
    with open(env_file, 'r') as f:
        content = f.read()
    
    linkedin_client_id = None
    linkedin_client_secret = None
    
    for line in content.split('\n'):
        if line.startswith('LINKEDIN_CLIENT_ID='):
            linkedin_client_id = line.split('=', 1)[1].strip()
        elif line.startswith('LINKEDIN_CLIENT_SECRET='):
            linkedin_client_secret = line.split('=', 1)[1].strip()
    
    if not linkedin_client_id or linkedin_client_id == 'your-linkedin-client-id-here':
        print("❌ LINKEDIN_CLIENT_ID not set or still has placeholder value")
        return False
    
    if not linkedin_client_secret or linkedin_client_secret == 'your-linkedin-client-secret-here':
        print("❌ LINKEDIN_CLIENT_SECRET not set or still has placeholder value")
        return False
    
    print("✅ LinkedIn credentials found in .env file")
    print(f"   Client ID: {linkedin_client_id[:10]}...")
    print(f"   Client Secret: {linkedin_client_secret[:10]}...")
    
    return True

def test_linkedin_auth_url():
    """Test generating LinkedIn auth URL."""
    print("\n🔗 Testing LinkedIn auth URL generation...")
    
    try:
        from config import settings
        
        # Check if credentials are loaded
        if not settings.linkedin_client_id:
            print("❌ LinkedIn Client ID not loaded from config")
            return False
        
        if not settings.linkedin_client_secret:
            print("❌ LinkedIn Client Secret not loaded from config")
            return False
        
        # Generate auth URL
        params = {
            "response_type": "code",
            "client_id": settings.linkedin_client_id,
            "redirect_uri": settings.linkedin_redirect_uri,
            "scope": settings.linkedin_scope,
            "state": "test_state"
        }
        
        query_string = urlencode(params)
        auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{query_string}"
        
        print("✅ LinkedIn auth URL generated successfully")
        print(f"   Auth URL: {auth_url}")
        
        # Check if URL looks correct
        if "linkedin.com/oauth/v2/authorization" in auth_url:
            print("✅ Auth URL format is correct")
            return True
        else:
            print("❌ Auth URL format is incorrect")
            return False
            
    except ImportError as e:
        print(f"❌ Error importing config: {e}")
        return False
    except Exception as e:
        print(f"❌ Error generating auth URL: {e}")
        return False

def check_redirect_uri():
    """Check if redirect URI is properly configured."""
    print("\n🔄 Checking redirect URI configuration...")
    
    try:
        from config import settings
        
        redirect_uri = settings.linkedin_redirect_uri
        print(f"   Configured redirect URI: {redirect_uri}")
        
        # Check if it matches expected format
        expected_uris = [
            "http://localhost:3000/linkedin-callback",
            "http://localhost:5173/linkedin-callback"
        ]
        
        if redirect_uri in expected_uris:
            print("✅ Redirect URI is correctly configured")
            return True
        else:
            print("⚠️  Redirect URI may not match LinkedIn app configuration")
            print("   Make sure your LinkedIn app has this redirect URI:")
            print(f"   {redirect_uri}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking redirect URI: {e}")
        return False

def main():
    """Main test function."""
    print("🔧 LinkedIn Configuration Test")
    print("=" * 40)
    
    # Check .env file
    env_ok = check_env_file()
    
    if not env_ok:
        print("\n❌ Environment configuration issues found!")
        print("   Please follow the setup guide in LINKEDIN_SETUP_GUIDE.md")
        return False
    
    # Test auth URL generation
    auth_ok = test_linkedin_auth_url()
    
    # Check redirect URI
    redirect_ok = check_redirect_uri()
    
    print("\n" + "=" * 40)
    
    if env_ok and auth_ok and redirect_ok:
        print("✅ All LinkedIn configuration tests passed!")
        print("\n📋 Next steps:")
        print("1. Make sure your LinkedIn app is approved")
        print("2. Verify redirect URI in LinkedIn app dashboard")
        print("3. Test the connection in your application")
        return True
    else:
        print("❌ Some configuration issues found!")
        print("\n🔧 To fix:")
        print("1. Check your .env file has correct LinkedIn credentials")
        print("2. Verify LinkedIn app configuration")
        print("3. Follow the setup guide in LINKEDIN_SETUP_GUIDE.md")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 