#!/usr/bin/env python3
"""
Test OAuth flow configuration
"""

import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.linkedin_service import linkedin_service
from config import settings

def test_oauth_configuration():
    """Test OAuth configuration."""
    print("🔧 Testing LinkedIn OAuth Configuration")
    print("=" * 50)
    
    # Test configuration
    print(f"Client ID: {settings.linkedin_client_id[:10]}...")
    print(f"Client Secret: {settings.linkedin_client_secret[:10]}...")
    print(f"Redirect URI: {settings.linkedin_redirect_uri}")
    print(f"Scope: {settings.linkedin_scope}")
    
    # Test auth URL generation
    print("\n🔧 Testing Auth URL Generation")
    print("=" * 40)
    
    try:
        auth_url = linkedin_service.get_auth_url("test_state")
        print(f"✅ Auth URL generated: {auth_url[:100]}...")
        
        # Check if redirect URI is correct
        if "redirect_uri=http%3A//localhost%3A3000/platforms" in auth_url:
            print("✅ Redirect URI is correctly set to /platforms")
        else:
            print("❌ Redirect URI is not correctly set")
            print(f"   Expected: http://localhost:3000/platforms")
            print(f"   Found in URL: {auth_url}")
            
    except Exception as e:
        print(f"❌ Error generating auth URL: {e}")
    
    print("\n" + "=" * 50)
    print("OAuth configuration test completed!")

if __name__ == "__main__":
    test_oauth_configuration() 