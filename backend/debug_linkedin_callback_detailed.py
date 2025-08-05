#!/usr/bin/env python3
"""
Detailed debug script for LinkedIn callback with working MongoDB
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_database, USERS_COLLECTION, PLATFORM_CONNECTIONS_COLLECTION
from utils.linkedin_service import linkedin_service
from config import settings

async def check_database_and_users():
    """Check database connection and users."""
    print("🔧 Checking Database and Users")
    print("=" * 50)
    
    try:
        db = get_database()
        
        # Test database connection
        await db.command("ping")
        print("✅ Database connection successful")
        
        # Check users
        user_count = await db[USERS_COLLECTION].count_documents({})
        print(f"✅ Users collection has {user_count} users")
        
        if user_count > 0:
            # Get first user for testing
            user = await db[USERS_COLLECTION].find_one({})
            print(f"✅ Sample user: {user.get('email', 'No email')}")
            return user
        else:
            print("⚠️  No users found in database")
            return None
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None

async def test_linkedin_service_methods():
    """Test LinkedIn service methods."""
    print("\n🔧 Testing LinkedIn Service Methods")
    print("=" * 50)
    
    print(f"Client ID: {settings.linkedin_client_id}")
    print(f"Client Secret: {settings.linkedin_client_secret[:10]}...")
    print(f"Redirect URI: {settings.linkedin_redirect_uri}")
    print(f"Scope: {settings.linkedin_scope}")
    
    # Test auth URL generation
    try:
        auth_url = linkedin_service.get_auth_url("test_state")
        print(f"✅ Auth URL generated: {auth_url[:100]}...")
    except Exception as e:
        print(f"❌ Error generating auth URL: {e}")
    
    # Test token exchange with invalid code (should fail gracefully)
    try:
        print("\n🧪 Testing token exchange with invalid code...")
        token_data = await linkedin_service.exchange_code_for_token("invalid_code")
        if token_data is None:
            print("✅ Token exchange correctly returns None for invalid code")
        else:
            print("⚠️  Token exchange returned data for invalid code")
    except Exception as e:
        print(f"❌ Token exchange error: {e}")

async def check_platform_connections():
    """Check existing platform connections."""
    print("\n🔧 Checking Platform Connections")
    print("=" * 50)
    
    try:
        db = get_database()
        
        # Check LinkedIn connections
        linkedin_connections = await db[PLATFORM_CONNECTIONS_COLLECTION].find(
            {"platform": "linkedin"}
        ).to_list(length=None)
        
        print(f"✅ Found {len(linkedin_connections)} LinkedIn connections")
        
        for conn in linkedin_connections:
            user = await db[USERS_COLLECTION].find_one({"_id": conn["user_id"]})
            print(f"   - User: {user.get('email', 'Unknown') if user else 'Unknown'}")
            print(f"     Connected: {conn.get('is_connected', False)}")
            print(f"     Has token: {bool(conn.get('access_token'))}")
            
    except Exception as e:
        print(f"❌ Error checking platform connections: {e}")

def show_possible_issues():
    """Show possible issues and solutions."""
    print("\n📝 Possible Issues and Solutions")
    print("=" * 50)
    print("Since MongoDB is working, the 400 error could be caused by:")
    print()
    print("1. 🔑 JWT Token Issues:")
    print("   - Token might be expired")
    print("   - Token might be invalid")
    print("   - User might not exist in database")
    print("   Solution: Log out and log back in")
    print()
    print("2. 🔗 LinkedIn Service Issues:")
    print("   - LinkedIn API might be rejecting the auth code")
    print("   - Auth code might be expired")
    print("   - LinkedIn service might have errors")
    print("   Solution: Check backend logs for LinkedIn API errors")
    print()
    print("3. 📋 Request Format Issues:")
    print("   - Frontend might be sending wrong data format")
    print("   - Missing required fields")
    print("   Solution: Check browser console for request details")
    print()
    print("4. 🔄 State Mismatch:")
    print("   - OAuth state parameter might not match")
    print("   - Session might be invalid")
    print("   Solution: Clear browser cache and try again")

async def main():
    """Main function."""
    print("LinkedIn Callback Detailed Debug")
    print("=" * 50)
    
    user = await check_database_and_users()
    await test_linkedin_service_methods()
    await check_platform_connections()
    show_possible_issues()
    
    print("\n🔧 Next Steps:")
    print("1. Check the backend server logs when you try LinkedIn Connect")
    print("2. Look for specific error messages in the logs")
    print("3. Try logging out and logging back in")
    print("4. Clear browser cache and cookies")

if __name__ == "__main__":
    asyncio.run(main()) 