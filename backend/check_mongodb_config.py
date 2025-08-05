#!/usr/bin/env python3
"""
Check MongoDB configuration and connection
"""

import os
import sys

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_env_file():
    """Check .env file for MongoDB configuration."""
    print("🔧 Checking .env file for MongoDB configuration")
    print("=" * 50)
    
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_file_path):
        print("❌ .env file not found!")
        return
    
    try:
        with open(env_file_path, 'r') as f:
            content = f.read()
        
        print("✅ .env file found")
        
        # Look for MongoDB URL
        lines = content.split('\n')
        mongodb_url = None
        
        for line in lines:
            if line.startswith('MONGODB_URL='):
                mongodb_url = line.split('=', 1)[1].strip()
                break
        
        if mongodb_url:
            print(f"✅ MongoDB URL found: {mongodb_url[:50]}...")
            if 'mongodb+srv://' in mongodb_url:
                print("✅ Using MongoDB Atlas (cloud)")
            elif 'mongodb://localhost' in mongodb_url:
                print("✅ Using local MongoDB")
            else:
                print("⚠️  Unknown MongoDB URL format")
        else:
            print("❌ MONGODB_URL not found in .env file")
            
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")

def check_config_loading():
    """Check if config is loading correctly."""
    print("\n🔧 Checking Config Loading")
    print("=" * 50)
    
    try:
        from config import settings
        print("✅ Config loaded successfully")
        print(f"   MongoDB URL: {settings.mongodb_url}")
        print(f"   Database Name: {settings.database_name}")
        
    except Exception as e:
        print(f"❌ Error loading config: {e}")

def check_database_connection():
    """Check database connection."""
    print("\n🔧 Checking Database Connection")
    print("=" * 50)
    
    try:
        from database import get_database
        
        # Try to get database connection
        db = get_database()
        print("✅ Database connection object created")
        
        # Try to access a collection
        users_collection = db.users
        print("✅ Users collection accessed")
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")

def main():
    """Main function."""
    print("MongoDB Configuration Check")
    print("=" * 50)
    
    check_env_file()
    check_config_loading()
    check_database_connection()
    
    print("\n📝 Summary:")
    print("If you see database connection errors but signup/login works,")
    print("it means the server is using a different configuration than")
    print("the scripts. The server might be loading the config differently.")

if __name__ == "__main__":
    main() 