#!/usr/bin/env python3
"""
Check backend status and database connection
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_database, USERS_COLLECTION

async def check_database():
    """Check database connection and users collection."""
    print("🔧 Checking Database Connection")
    print("=" * 50)
    
    try:
        db = get_database()
        
        # Test database connection
        await db.command("ping")
        print("✅ Database connection successful")
        
        # Check if users collection exists and has data
        user_count = await db[USERS_COLLECTION].count_documents({})
        print(f"✅ Users collection has {user_count} users")
        
        if user_count == 0:
            print("⚠️  No users found in database")
            print("   You need to create a user account first")
        else:
            print("✅ Users exist in database")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("   Make sure MongoDB is running")

def show_solution():
    """Show solution steps."""
    print("\n📝 Solution Steps")
    print("=" * 50)
    print("1. 🔄 Log out of the frontend")
    print("2. 🔄 Log back in to get a fresh JWT token")
    print("3. 🧪 Try the LinkedIn Connect button again")
    print("4. 📋 If it still fails, check the backend logs")
    
    print("\n🔧 If the problem persists:")
    print("1. Check if MongoDB is running")
    print("2. Restart the backend server")
    print("3. Clear browser cache and cookies")
    print("4. Try a different browser")

async def main():
    """Main function."""
    print("Backend Status Check")
    print("=" * 50)
    
    await check_database()
    show_solution()

if __name__ == "__main__":
    asyncio.run(main()) 