#!/usr/bin/env python3
"""
Debug script to test LinkedIn API and identify issues with profile retrieval.
"""

import asyncio
import requests
import json
from config import settings

def test_linkedin_auth_url():
    """Test LinkedIn auth URL generation."""
    print("=== Testing LinkedIn Auth URL ===")
    
    client_id = settings.linkedin_client_id
    redirect_uri = settings.linkedin_redirect_uri
    scope = settings.linkedin_scope
    
    print(f"Client ID: {client_id}")
    print(f"Redirect URI: {redirect_uri}")
    print(f"Scope: {scope}")
    
    # Generate auth URL manually
    from urllib.parse import urlencode
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": "test_state"
    }
    
    query_string = urlencode(params)
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{query_string}"
    print(f"Generated Auth URL: {auth_url}")
    print()

def test_linkedin_token_exchange(auth_code):
    """Test LinkedIn token exchange."""
    print("=== Testing LinkedIn Token Exchange ===")
    
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": settings.linkedin_client_id,
        "client_secret": settings.linkedin_client_secret,
        "redirect_uri": settings.linkedin_redirect_uri
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    print(f"Token URL: {token_url}")
    print(f"Client ID: {settings.linkedin_client_id}")
    print(f"Redirect URI: {settings.linkedin_redirect_uri}")
    print(f"Auth Code (first 20 chars): {auth_code[:20]}...")
    
    try:
        response = requests.post(token_url, data=data, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Token exchange successful!")
            print(f"Access Token (first 20 chars): {token_data.get('access_token', '')[:20]}...")
            print(f"Expires In: {token_data.get('expires_in')}")
            return token_data.get('access_token')
        else:
            print("❌ Token exchange failed!")
            print(f"Response Body: {response.text}")
            try:
                error_json = response.json()
                print(f"Error Details: {json.dumps(error_json, indent=2)}")
            except:
                print("Could not parse error response as JSON")
            return None
            
    except Exception as e:
        print(f"❌ Exception during token exchange: {e}")
        return None

def test_linkedin_profile(access_token):
    """Test LinkedIn profile retrieval."""
    print("\n=== Testing LinkedIn Profile Retrieval ===")
    
    if not access_token:
        print("❌ No access token provided")
        return
    
    # Test different endpoints and headers
    endpoints = [
        "https://api.linkedin.com/v2/me",
        "https://api.linkedin.com/v2/me?projection=(id,localizedFirstName,localizedLastName)",
        "https://api.linkedin.com/v2/me?projection=(id,firstName,lastName)"
    ]
    
    headers_variations = [
        {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        },
        {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        },
        {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    ]
    
    for i, endpoint in enumerate(endpoints):
        print(f"\n--- Testing Endpoint {i+1}: {endpoint} ---")
        
        for j, headers in enumerate(headers_variations):
            print(f"  Headers variation {j+1}: {headers}")
            
            try:
                response = requests.get(endpoint, headers=headers)
                print(f"  Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    profile_data = response.json()
                    print(f"  ✅ Success! Profile data: {json.dumps(profile_data, indent=2)}")
                    return profile_data
                else:
                    print(f"  ❌ Failed! Response: {response.text}")
                    
            except Exception as e:
                print(f"  ❌ Exception: {e}")
    
    print("\n❌ All profile retrieval attempts failed")

def main():
    """Main function to run all tests."""
    print("🔍 LinkedIn API Debug Tool")
    print("=" * 50)
    
    # Test auth URL generation
    test_linkedin_auth_url()
    
    # Ask for auth code if user wants to test token exchange
    print("\n" + "=" * 50)
    auth_code = input("Enter LinkedIn auth code to test token exchange (or press Enter to skip): ").strip()
    
    if auth_code:
        access_token = test_linkedin_token_exchange(auth_code)
        if access_token:
            test_linkedin_profile(access_token)
    else:
        print("Skipping token exchange and profile tests.")
        print("\nTo get an auth code:")
        print("1. Visit the auth URL above")
        print("2. Complete the LinkedIn OAuth flow")
        print("3. Copy the 'code' parameter from the callback URL")
        print("4. Run this script again with the auth code")

if __name__ == "__main__":
    main() 