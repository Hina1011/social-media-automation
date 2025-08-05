#!/usr/bin/env python3
"""
Comprehensive scope fix script
"""

import os
import re

def fix_all_scope_issues():
    """Fix all scope-related issues."""
    print("🔧 Comprehensive Scope Fix")
    print("=" * 50)
    
    # Fix .env file
    fix_env_file()
    
    # Fix config.py if needed
    fix_config_file()
    
    print("\n✅ All scope issues should be fixed!")
    print("Please restart your server and try the LinkedIn Connect button again.")

def fix_env_file():
    """Fix the .env file."""
    print("\n1. Fixing .env file...")
    
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_file_path):
        print("   ❌ .env file not found!")
        return
    
    try:
        with open(env_file_path, 'r') as f:
            content = f.read()
        
        # Replace any scope-related lines
        new_content = re.sub(
            r'LINKEDIN_SCOPE\s*=\s*.+',
            'LINKEDIN_SCOPE=openid',
            content,
            flags=re.MULTILINE
        )
        
        # Write back
        with open(env_file_path, 'w') as f:
            f.write(new_content)
        
        print("   ✅ .env file updated")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

def fix_config_file():
    """Fix the config.py file."""
    print("\n2. Checking config.py...")
    
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.py')
    
    try:
        with open(config_file_path, 'r') as f:
            content = f.read()
        
        # Check if scope is already correct
        if 'linkedin_scope: str = "openid"' in content:
            print("   ✅ config.py scope is already correct")
        else:
            # Replace the scope line
            new_content = re.sub(
                r'linkedin_scope: str = "[^"]*"',
                'linkedin_scope: str = "openid"',
                content
            )
            
            with open(config_file_path, 'w') as f:
                f.write(new_content)
            
            print("   ✅ config.py updated")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

def show_manual_instructions():
    """Show manual instructions."""
    print("\n📝 Manual Fix Instructions:")
    print("=" * 50)
    print("If automatic fix didn't work, manually update:")
    print()
    print("1. In your .env file, change:")
    print("   LINKEDIN_SCOPE=r_liteprofile r_emailaddress w_member_social")
    print("   to:")
    print("   LINKEDIN_SCOPE=openid")
    print()
    print("2. In your config.py file, change:")
    print('   linkedin_scope: str = "r_liteprofile r_emailaddress w_member_social"')
    print("   to:")
    print('   linkedin_scope: str = "openid"')
    print()
    print("3. Restart your server:")
    print("   python start_server.py")
    print()
    print("4. Test the LinkedIn Connect button")

def main():
    """Main function."""
    print("LinkedIn Scope Fix Tool")
    print("=" * 50)
    
    fix_all_scope_issues()
    show_manual_instructions()

if __name__ == "__main__":
    main() 