#!/usr/bin/env python3
"""
Script to fix .env file scope issue
"""

import os
import re

def fix_env_file():
    """Fix the .env file scope configuration."""
    print("🔧 Fixing .env file scope configuration")
    print("=" * 50)
    
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_file_path):
        print("❌ .env file not found!")
        print(f"   Expected location: {env_file_path}")
        return
    
    # Read the current .env file
    try:
        with open(env_file_path, 'r') as f:
            content = f.read()
        
        print("✅ .env file found and read successfully")
        
        # Check current scope
        scope_match = re.search(r'LINKEDIN_SCOPE=(.+)', content)
        if scope_match:
            current_scope = scope_match.group(1).strip()
            print(f"   Current scope: {current_scope}")
            
            if current_scope == "openid":
                print("   ✅ Scope is already correct!")
                return
            else:
                print("   ❌ Scope needs to be updated")
        else:
            print("   ❌ LINKEDIN_SCOPE not found in .env file")
            return
        
        # Replace the scope
        new_content = re.sub(
            r'LINKEDIN_SCOPE=.+',
            'LINKEDIN_SCOPE=openid',
            content
        )
        
        # Write the updated content back
        with open(env_file_path, 'w') as f:
            f.write(new_content)
        
        print("✅ .env file updated successfully!")
        print("   Scope changed to: openid")
        
        # Verify the change
        with open(env_file_path, 'r') as f:
            new_content = f.read()
        
        scope_match = re.search(r'LINKEDIN_SCOPE=(.+)', new_content)
        if scope_match:
            new_scope = scope_match.group(1).strip()
            print(f"   Verified new scope: {new_scope}")
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")

def show_env_instructions():
    """Show manual instructions for updating .env file."""
    print("\n📝 Manual .env File Update Instructions:")
    print("=" * 50)
    print("If the automatic fix didn't work, manually edit your .env file:")
    print()
    print("1. Open your .env file in a text editor")
    print("2. Find this line:")
    print("   LINKEDIN_SCOPE=r_liteprofile r_emailaddress w_member_social")
    print()
    print("3. Change it to:")
    print("   LINKEDIN_SCOPE=openid")
    print()
    print("4. Save the file")
    print("5. Restart your server")
    print()
    print("6. Test again with:")
    print("   python test_oauth_flow.py")

def main():
    """Main function."""
    print("LinkedIn Scope Fix Tool")
    print("=" * 50)
    
    fix_env_file()
    show_env_instructions()

if __name__ == "__main__":
    main() 