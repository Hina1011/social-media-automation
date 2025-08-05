#!/usr/bin/env python3
"""
Debug the entire LinkedIn OAuth flow
"""

import requests
import json
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.linkedin_service import linkedin_service
from config import settings

def test_linkedin_service():
    """Test LinkedIn service methods."""
    print("🔧 Testing LinkedIn Service")
    print("=" * 50)
    
    print(f"Client ID: {settings.linkedin_client_id}")
    print(f"Client Secret: {settings.linkedin_client_secret[:10]}...")
    print(f"Redirect URI: {settings.linkedin_redirect_uri}")
    print(f"Scope: {settings.linkedin_scope}")
    
    # Test auth URL generation
    try:
        auth_url = linkedin_service.get_auth_url("test_state")
        print(f"\n✅ Auth URL generated: {auth_url[:100]}...")
        
        # Check if redirect URI is correct
        if "redirect_uri=http%3A//localhost%3A3000/platforms" in auth_url:
            print("✅ Redirect URI is correctly set to /platforms")
        else:
            print("❌ Redirect URI is not correctly set")
            
    except Exception as e:
        print(f"❌ Error generating auth URL: {e}")

def test_backend_endpoints():
    """Test backend endpoints."""
    print("\n🔧 Testing Backend Endpoints")
    print("=" * 50)
    
    # Test if server is running
    try:
        response = requests.get("http://localhost:8000/")
        print(f"✅ Server is running (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running on port 8000")
        return
    
    # Test LinkedIn auth URL endpoint
    try:
        response = requests.get("http://localhost:8000/api/platforms/linkedin/auth-url")
        print(f"✅ LinkedIn auth URL endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Auth URL: {data.get('auth_url', '')[:100]}...")
    except Exception as e:
        print(f"❌ LinkedIn auth URL endpoint error: {e}")
    
    # Test platforms endpoint
    try:
        response = requests.get("http://localhost:8000/api/platforms")
        print(f"✅ Platforms endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Platforms endpoint error: {e}")

def show_troubleshooting_steps():
    """Show troubleshooting steps."""
    print("\n📝 Troubleshooting Steps")
    print("=" * 50)
    print("1. ✅ OAuth flow is working (you reached LinkedIn's authorization page)")
    print("2. ✅ Authorization was successful (you clicked 'Allow')")
    print("3. ❌ Callback is failing (400 Bad Request)")
    print("\nPossible causes:")
    print("- JWT token might be expired or invalid")
    print("- User might not exist in the database")
    print("- LinkedIn service might be failing to exchange the auth code")
    print("- Database connection issues")
    
    print("\n🔧 Debug Steps:")
    print("1. Check if you're logged in to the frontend")
    print("2. Check if your JWT token is valid")
    print("3. Check the backend logs for detailed error messages")
    print("4. Try logging out and logging back in")
    print("5. Check if MongoDB is running")

def main():
    """Main function."""
    print("LinkedIn OAuth Flow Debug Tool")
    print("=" * 50)
    
    test_linkedin_service()
    test_backend_endpoints()
    show_troubleshooting_steps()

if __name__ == "__main__":
    main() 