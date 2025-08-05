#!/usr/bin/env python3
"""
LinkedIn App Configuration Checker
"""

import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings

def check_linkedin_app_config():
    """Check LinkedIn app configuration."""
    print("🔧 LinkedIn App Configuration Check")
    print("=" * 50)
    
    print("\n1. Current Configuration:")
    print(f"   Client ID: {settings.linkedin_client_id}")
    print(f"   Client Secret: {settings.linkedin_client_secret[:10]}...")
    print(f"   Redirect URI: {settings.linkedin_redirect_uri}")
    print(f"   Scope: {settings.linkedin_scope}")
    
    print("\n2. Configuration Validation:")
    
    # Check if credentials are set
    if not settings.linkedin_client_id or settings.linkedin_client_id == "":
        print("   ❌ Client ID is not set")
    else:
        print("   ✅ Client ID is configured")
    
    if not settings.linkedin_client_secret or settings.linkedin_client_secret == "":
        print("   ❌ Client Secret is not set")
    else:
        print("   ✅ Client Secret is configured")
    
    # Check redirect URI
    if settings.linkedin_redirect_uri == "http://localhost:3000/platforms":
        print("   ✅ Redirect URI is correctly set to /platforms")
    else:
        print(f"   ❌ Redirect URI should be: http://localhost:3000/platforms")
        print(f"      Current: {settings.linkedin_redirect_uri}")
    
    # Check scope
    required_scopes = ["r_liteprofile", "r_emailaddress", "w_member_social"]
    current_scopes = settings.linkedin_scope.split()
    
    print("\n3. Required Scopes Check:")
    for scope in required_scopes:
        if scope in current_scopes:
            print(f"   ✅ {scope}")
        else:
            print(f"   ❌ {scope} - Missing")
    
    print("\n4. LinkedIn App Setup Checklist:")
    print("   [ ] Go to https://www.linkedin.com/developers/")
    print("   [ ] Select your app")
    print("   [ ] Go to 'Auth' tab")
    print("   [ ] Verify redirect URI matches: http://localhost:3000/platforms")
    print("   [ ] Check that all required scopes are added")
    print("   [ ] Ensure app is active and not in development mode")
    print("   [ ] Add your email as a test user if needed")
    
    print("\n5. Browser Troubleshooting:")
    print("   [ ] Clear browser cache and cookies")
    print("   [ ] Try incognito/private mode")
    print("   [ ] Disable browser extensions")
    print("   [ ] Try a different browser")
    print("   [ ] Wait a few minutes and try again")
    
    print("\n6. If OAuth still fails:")
    print("   [ ] Use the manual token method")
    print("   [ ] Run: python add_linkedin_token.py")
    print("   [ ] Add your access token to .env file")
    
    print("\n" + "=" * 50)
    print("Configuration check completed!")

if __name__ == "__main__":
    check_linkedin_app_config() 