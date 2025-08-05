#!/usr/bin/env python3
"""
Update .env file with correct LinkedIn scopes
"""

import os
import re

def update_env_scopes():
    """Update .env file with correct LinkedIn scopes."""
    print("🔧 Updating .env file with correct LinkedIn scopes")
    print("=" * 60)
    
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_file_path):
        print("❌ .env file not found!")
        return
    
    try:
        # Read current .env file
        with open(env_file_path, 'r') as f:
            content = f.read()
        
        print("✅ .env file found")
        
        # Check current scope
        scope_match = re.search(r'LINKEDIN_SCOPE\s*=\s*(.+)', content)
        if scope_match:
            current_scope = scope_match.group(1).strip()
            print(f"   Current scope: {current_scope}")
        
        # Update to match LinkedIn app scopes
        correct_scope = "openid profile w_member_social email"
        
        # Replace the scope line
        new_content = re.sub(
            r'LINKEDIN_SCOPE\s*=\s*.+',
            f'LINKEDIN_SCOPE={correct_scope}',
            content,
            flags=re.MULTILINE
        )
        
        # Write back
        with open(env_file_path, 'w') as f:
            f.write(new_content)
        
        print(f"✅ .env file updated with scope: {correct_scope}")
        print("   This matches your LinkedIn app's registered scopes")
        
        # Verify
        with open(env_file_path, 'r') as f:
            new_content = f.read()
        
        scope_match = re.search(r'LINKEDIN_SCOPE\s*=\s*(.+)', new_content)
        if scope_match:
            new_scope = scope_match.group(1).strip()
            print(f"   Verified new scope: {new_scope}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def show_next_steps():
    """Show next steps."""
    print("\n📝 Next Steps:")
    print("=" * 60)
    print("1. ✅ .env file updated")
    print("2. ✅ config.py updated")
    print("3. 🔄 Restart your server:")
    print("   python start_server.py")
    print("4. 🧪 Test the configuration:")
    print("   python test_oauth_flow.py")
    print("5. 🚀 Try LinkedIn Connect button again")

def main():
    """Main function."""
    print("LinkedIn Scope Update Tool")
    print("=" * 60)
    
    update_env_scopes()
    show_next_steps()

if __name__ == "__main__":
    main() 