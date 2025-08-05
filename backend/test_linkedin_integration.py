#!/usr/bin/env python3
"""
Test script for LinkedIn integration
"""

import asyncio
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword123"

def test_linkedin_endpoints():
    """Test LinkedIn integration endpoints"""
    
    print("🔗 Testing LinkedIn Integration")
    print("=" * 50)
    
    # 1. Test LinkedIn auth URL generation
    print("\n1. Testing LinkedIn Auth URL generation...")
    try:
        # First, we need to get a valid token
        login_response = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            return
        
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test auth URL generation
        auth_url_response = requests.get(f"{BASE_URL}/api/platforms/linkedin/auth-url", headers=headers)
        
        if auth_url_response.status_code == 200:
            auth_data = auth_url_response.json()
            print(f"✅ Auth URL generated successfully")
            print(f"   Auth URL: {auth_data.get('auth_url', 'N/A')}")
            print(f"   State: {auth_data.get('state', 'N/A')}")
        else:
            print(f"❌ Auth URL generation failed: {auth_url_response.status_code}")
            print(f"   Response: {auth_url_response.text}")
            
    except Exception as e:
        print(f"❌ Error testing auth URL: {e}")
    
    # 2. Test platform status
    print("\n2. Testing platform status...")
    try:
        status_response = requests.get(f"{BASE_URL}/api/platforms/status", headers=headers)
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"✅ Platform status retrieved")
            print(f"   LinkedIn connected: {status_data.get('linkedin', False)}")
            print(f"   Instagram connected: {status_data.get('instagram', False)}")
            print(f"   Facebook connected: {status_data.get('facebook', False)}")
            print(f"   Twitter connected: {status_data.get('twitter', False)}")
        else:
            print(f"❌ Platform status failed: {status_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing platform status: {e}")
    
    # 3. Test platform connections
    print("\n3. Testing platform connections...")
    try:
        connections_response = requests.get(f"{BASE_URL}/api/platforms", headers=headers)
        
        if connections_response.status_code == 200:
            connections = connections_response.json()
            print(f"✅ Platform connections retrieved")
            print(f"   Total connections: {len(connections)}")
            for conn in connections:
                print(f"   - {conn.get('platform')}: {conn.get('is_connected', False)}")
        else:
            print(f"❌ Platform connections failed: {connections_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing platform connections: {e}")
    
    # 4. Test LinkedIn posting (if connected)
    print("\n4. Testing LinkedIn posting...")
    try:
        # Check if LinkedIn is connected
        status_response = requests.get(f"{BASE_URL}/api/platforms/status", headers=headers)
        if status_response.status_code == 200:
            status_data = status_response.json()
            if status_data.get('linkedin', False):
                # Test posting to LinkedIn
                post_data = {
                    "content": "Test post from social media automation platform! 🚀 #testing #automation",
                    "image_url": None
                }
                
                post_response = requests.post(f"{BASE_URL}/api/platforms/linkedin/post", 
                                           headers=headers, json=post_data)
                
                if post_response.status_code == 200:
                    result = post_response.json()
                    print(f"✅ LinkedIn posting successful")
                    print(f"   Post ID: {result.get('linkedin_post_id', 'N/A')}")
                    print(f"   Message: {result.get('message', 'N/A')}")
                else:
                    print(f"❌ LinkedIn posting failed: {post_response.status_code}")
                    print(f"   Response: {post_response.text}")
            else:
                print("⚠️ LinkedIn not connected - skipping posting test")
        else:
            print(f"❌ Could not check LinkedIn status: {status_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing LinkedIn posting: {e}")
    
    print("\n" + "=" * 50)
    print("✅ LinkedIn integration test completed!")

def test_linkedin_service():
    """Test LinkedIn service directly"""
    
    print("\n🔧 Testing LinkedIn Service")
    print("=" * 50)
    
    try:
        from utils.linkedin_service import linkedin_service
        
        # Test auth URL generation
        print("\n1. Testing LinkedIn service auth URL...")
        auth_url = linkedin_service.get_auth_url("test_state")
        print(f"✅ Auth URL: {auth_url}")
        
        # Test service initialization
        print(f"\n2. LinkedIn service configuration:")
        print(f"   Client ID: {'Set' if linkedin_service.client_id else 'Not set'}")
        print(f"   Client Secret: {'Set' if linkedin_service.client_secret else 'Not set'}")
        print(f"   Redirect URI: {linkedin_service.redirect_uri}")
        print(f"   Scope: {linkedin_service.scope}")
        
    except ImportError as e:
        print(f"❌ Could not import LinkedIn service: {e}")
    except Exception as e:
        print(f"❌ Error testing LinkedIn service: {e}")

if __name__ == "__main__":
    print("🚀 Starting LinkedIn Integration Tests")
    print("Make sure your backend server is running on http://localhost:8000")
    print("Make sure you have set up your LinkedIn API credentials in .env")
    
    # Test LinkedIn service
    test_linkedin_service()
    
    # Test API endpoints
    test_linkedin_endpoints()
    
    print("\n📝 Next Steps:")
    print("1. Set up your LinkedIn Developer App")
    print("2. Add your LinkedIn credentials to .env file")
    print("3. Test the OAuth flow in your frontend")
    print("4. Verify posting functionality") 