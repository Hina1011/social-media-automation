#!/usr/bin/env python3
"""
Simple script to test .env file reading
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("🔧 Testing .env file configuration")
print("=" * 50)

# Test LinkedIn configuration
linkedin_client_id = os.getenv("LINKEDIN_CLIENT_ID")
linkedin_client_secret = os.getenv("LINKEDIN_CLIENT_SECRET")
linkedin_access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
linkedin_refresh_token = os.getenv("LINKEDIN_REFRESH_TOKEN")

print(f"LinkedIn Client ID: {'✅ Set' if linkedin_client_id else '❌ Not set'}")
print(f"LinkedIn Client Secret: {'✅ Set' if linkedin_client_secret else '❌ Not set'}")
print(f"LinkedIn Access Token: {'✅ Set' if linkedin_access_token else '❌ Not set'}")
print(f"LinkedIn Refresh Token: {'✅ Set' if linkedin_refresh_token else '❌ Not set'}")

if linkedin_access_token:
    print(f"\nAccess Token (first 20 chars): {linkedin_access_token[:20]}...")
    print("✅ Your LinkedIn access token is configured!")

print("\n.env file test completed!") 