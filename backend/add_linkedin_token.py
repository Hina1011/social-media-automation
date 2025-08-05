#!/usr/bin/env python3
"""
Script to manually add LinkedIn access token to the database
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from bson import ObjectId

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_database, PLATFORM_CONNECTIONS_COLLECTION
from config import settings

async def add_linkedin_token():
    """Add LinkedIn access token manually to the database."""
    
    print("🔧 LinkedIn Token Manual Addition")
    print("=" * 50)
    
    # Get user input
    user_email = input("Enter your email address: ").strip()
    access_token = input("Enter your LinkedIn access token: ").strip()
    refresh_token = input("Enter your LinkedIn refresh token (optional, press Enter to skip): ").strip()
    
    if not user_email or not access_token:
        print("❌ Email and access token are required!")
        return
    
    # Get database connection
    db = get_database()
    
    # Find user by email
    user = await db.users.find_one({"email": user_email})
    if not user:
        print(f"❌ User with email '{user_email}' not found!")
        return
    
    print(f"✅ Found user: {user.get('name', 'Unknown')}")
    
    # Calculate expiration (LinkedIn tokens typically expire in 60 days)
    expires_at = datetime.utcnow() + timedelta(days=60)
    
    # Prepare connection document
    connection_doc = {
        "user_id": ObjectId(user["_id"]),
        "platform": "linkedin",
        "is_connected": True,
        "platform_user_id": None,  # Will be updated when we get profile info
        "platform_username": None,  # Will be updated when we get profile info
        "access_token": access_token,
        "refresh_token": refresh_token if refresh_token else None,
        "expires_at": expires_at,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Upsert the connection
    result = await db[PLATFORM_CONNECTIONS_COLLECTION].replace_one(
        {
            "user_id": ObjectId(user["_id"]),
            "platform": "linkedin"
        },
        connection_doc,
        upsert=True
    )
    
    if result.upserted_id or result.modified_count > 0:
        print("✅ LinkedIn token added successfully!")
        print(f"   User ID: {user['_id']}")
        print(f"   Platform: LinkedIn")
        print(f"   Expires at: {expires_at}")
        
        # Try to get user profile to update username
        try:
            from utils.linkedin_service import linkedin_service
            profile_data = await linkedin_service.get_user_profile(access_token)
            if profile_data:
                await db[PLATFORM_CONNECTIONS_COLLECTION].update_one(
                    {"_id": result.upserted_id or result.upserted_id},
                    {
                        "$set": {
                            "platform_user_id": profile_data.get("id"),
                            "platform_username": f"{profile_data.get('first_name', '')} {profile_data.get('last_name', '')}".strip()
                        }
                    }
                )
                print(f"   Profile: {profile_data.get('first_name', '')} {profile_data.get('last_name', '')}")
        except Exception as e:
            print(f"   Note: Could not fetch profile info: {e}")
    else:
        print("❌ Failed to add LinkedIn token!")

async def list_linkedin_connections():
    """List all LinkedIn connections in the database."""
    
    print("\n📋 Current LinkedIn Connections")
    print("=" * 50)
    
    db = get_database()
    connections = await db[PLATFORM_CONNECTIONS_COLLECTION].find(
        {"platform": "linkedin"}
    ).to_list(length=None)
    
    if not connections:
        print("No LinkedIn connections found.")
        return
    
    for conn in connections:
        user = await db.users.find_one({"_id": conn["user_id"]})
        print(f"User: {user.get('email', 'Unknown') if user else 'Unknown'}")
        print(f"  Connected: {conn.get('is_connected', False)}")
        print(f"  Username: {conn.get('platform_username', 'Not set')}")
        print(f"  Expires: {conn.get('expires_at', 'Not set')}")
        print(f"  Updated: {conn.get('updated_at', 'Not set')}")
        print("-" * 30)

def main():
    """Main function."""
    print("LinkedIn Token Management")
    print("1. Add LinkedIn token")
    print("2. List LinkedIn connections")
    
    choice = input("Choose an option (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(add_linkedin_token())
    elif choice == "2":
        asyncio.run(list_linkedin_connections())
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main() 