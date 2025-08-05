#!/usr/bin/env python3
"""
Start server script with MongoDB connection check
"""

import os
import sys
import subprocess
import time
from dotenv import load_dotenv

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'motor',
        'pymongo',
        'python-dotenv',
        'python-jose',
        'passlib',
        'python-multipart'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    return True

def check_env_file():
    """Check if .env file exists and has required variables."""
    print("\n🔍 Checking .env file...")
    
    load_dotenv()
    
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_file_path):
        print("❌ .env file not found")
        print("Creating .env file template...")
        create_env_template()
        return False
    
    mongodb_url = os.getenv("MONGODB_URL")
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    
    if not mongodb_url:
        print("❌ MONGODB_URL not set in .env file")
        return False
    
    if not jwt_secret:
        print("❌ JWT_SECRET_KEY not set in .env file")
        return False
    
    print("✅ .env file configured")
    return True

def create_env_template():
    """Create a .env file template."""
    env_content = """# MongoDB Configuration
MONGODB_URL=mongodb+srv://your_username:your_password@your_cluster.mongodb.net/your_database?retryWrites=true&w=majority
DATABASE_NAME=social_media_automation

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production

# Development Settings
DEBUG=True
"""
    
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    with open(env_file_path, 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file template")
    print("⚠️  Please edit the .env file with your actual MongoDB Atlas connection string")

def test_mongodb_connection():
    """Test MongoDB connection."""
    print("\n🔍 Testing MongoDB connection...")
    
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        import asyncio
        
        load_dotenv()
        mongodb_url = os.getenv("MONGODB_URL")
        
        if not mongodb_url:
            print("❌ MONGODB_URL not set")
            return False
        
        # Test connection
        if "mongodb+srv://" in mongodb_url or "mongodb.net" in mongodb_url:
            connection_string = mongodb_url
            if "?" not in connection_string:
                connection_string += "?ssl=true&tlsAllowInvalidCertificates=true"
            elif "ssl=true" not in connection_string:
                connection_string += "&ssl=true&tlsAllowInvalidCertificates=true"
            
            client = AsyncIOMotorClient(connection_string, tlsAllowInvalidCertificates=True)
        else:
            client = AsyncIOMotorClient(mongodb_url)
        
        async def test_connection():
            try:
                await client.admin.command('ping')
                client.close()
                return True
            except Exception as e:
                print(f"❌ Connection failed: {e}")
                return False
        
        success = asyncio.run(test_connection())
        if success:
            print("✅ MongoDB connection successful")
        return success
        
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def start_server():
    """Start the FastAPI server."""
    print("\n🚀 Starting server...")
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, 'main.py'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True

def main():
    """Main function."""
    print("🚀 Social Media Automation Platform - Server Startup")
    print("=" * 50)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return
    
    # Step 2: Check environment file
    if not check_env_file():
        print("❌ Environment file check failed")
        print("Please configure your .env file and try again")
        return
    
    # Step 3: Test MongoDB connection
    if not test_mongodb_connection():
        print("❌ MongoDB connection test failed")
        print("Please check your MongoDB Atlas connection string")
        return
    
    # Step 4: Start server
    print("\n✅ All checks passed!")
    print("Starting server on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    start_server()

if __name__ == "__main__":
    main() 