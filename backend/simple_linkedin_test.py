#!/usr/bin/env python3
"""
Simple LinkedIn configuration test
"""

import os
import sys

def test_env_file():
    """Test if .env file exists and can be read."""
    print("🔧 Testing .env file")
    print("=" * 30)
    
    # Check if .env file exists
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        print("✅ .env file found")
        
        # Try to read the file
        try:
            with open(env_path, 'r') as f:
                content = f.read()
                print(f"✅ .env file can be read ({len(content)} characters)")
                
                # Check for LinkedIn variables
                if 'LINKEDIN_ACCESS_TOKEN' in content:
                    print("✅ LINKEDIN_ACCESS_TOKEN found in .env file")
                else:
                    print("❌ LINKEDIN_ACCESS_TOKEN not found in .env file")
                    
                if 'LINKEDIN_CLIENT_ID' in content:
                    print("✅ LINKEDIN_CLIENT_ID found in .env file")
                else:
                    print("❌ LINKEDIN_CLIENT_ID not found in .env file")
                    
                if 'LINKEDIN_CLIENT_SECRET' in content:
                    print("✅ LINKEDIN_CLIENT_SECRET found in .env file")
                else:
                    print("❌ LINKEDIN_CLIENT_SECRET not found in .env file")
                    
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
    else:
        print("❌ .env file not found")
        print(f"   Expected location: {env_path}")

def test_config_file():
    """Test if config.py can be imported."""
    print("\n🔧 Testing config.py")
    print("=" * 30)
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(__file__))
        
        # Try to import config
        import config
        print("✅ config.py imported successfully")
        
        # Check LinkedIn settings
        if hasattr(config.settings, 'linkedin_client_id'):
            client_id = config.settings.linkedin_client_id
            if client_id and client_id != "":
                print(f"✅ LinkedIn Client ID: {client_id[:10]}...")
            else:
                print("❌ LinkedIn Client ID is empty")
        else:
            print("❌ LinkedIn Client ID not found in config")
            
        if hasattr(config.settings, 'linkedin_client_secret'):
            client_secret = config.settings.linkedin_client_secret
            if client_secret and client_secret != "":
                print(f"✅ LinkedIn Client Secret: {client_secret[:10]}...")
            else:
                print("❌ LinkedIn Client Secret is empty")
        else:
            print("❌ LinkedIn Client Secret not found in config")
            
    except Exception as e:
        print(f"❌ Error importing config: {e}")

def main():
    """Main test function."""
    print("LinkedIn Configuration Test")
    print("=" * 50)
    
    test_env_file()
    test_config_file()
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    main() 