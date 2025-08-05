#!/usr/bin/env python3
"""
Comprehensive LinkedIn API issue fixer and diagnostic tool.
"""

import os
import sys
import requests
import json
from config import settings

def check_linkedin_app_configuration():
    """Check LinkedIn app configuration and provide guidance."""
    print("🔍 LinkedIn App Configuration Check")
    print("=" * 50)
    
    print(f"Client ID: {settings.linkedin_client_id}")
    print(f"Redirect URI: {settings.linkedin_redirect_uri}")
    print(f"Scope: {settings.linkedin_scope}")
    
    # Check if credentials look valid
    if not settings.linkedin_client_id or settings.linkedin_client_id == "your-linkedin-client-id":
        print("❌ LinkedIn Client ID not configured properly")
        return False
    
    if not settings.linkedin_client_secret or settings.linkedin_client_secret == "your-linkedin-client-secret":
        print("❌ LinkedIn Client Secret not configured properly")
        return False
    
    print("✅ Basic configuration looks good")
    return True

def generate_linkedin_auth_url():
    """Generate LinkedIn auth URL for testing."""
    print("\n🔗 LinkedIn Auth URL Generation")
    print("=" * 50)
    
    from urllib.parse import urlencode
    params = {
        "response_type": "code",
        "client_id": settings.linkedin_client_id,
        "redirect_uri": settings.linkedin_redirect_uri,
        "scope": settings.linkedin_scope,
        "state": "test_state"
    }
    
    query_string = urlencode(params)
    auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{query_string}"
    
    print(f"Auth URL: {auth_url}")
    print("\n📋 Steps to test:")
    print("1. Copy the auth URL above")
    print("2. Open it in a browser")
    print("3. Complete the LinkedIn OAuth flow")
    print("4. Check if you get redirected to the callback URL")
    print("5. Look for any error messages")
    
    return auth_url

def test_linkedin_api_permissions():
    """Test if the LinkedIn app has the right permissions."""
    print("\n🔐 LinkedIn API Permissions Test")
    print("=" * 50)
    
    print("To check if your LinkedIn app has the right permissions:")
    print("\n1. Go to https://developer.linkedin.com/")
    print("2. Sign in and go to your app dashboard")
    print("3. Click on your app")
    print("4. Go to 'Products' tab")
    print("5. Check if you have access to:")
    print("   - Sign In with LinkedIn")
    print("   - Marketing Developer Platform")
    print("   - Share on LinkedIn")
    
    print("\n⚠️  Common Issues:")
    print("- App not approved for required permissions")
    print("- Missing 'Sign In with LinkedIn' product")
    print("- App in development mode (limited access)")
    print("- Incorrect redirect URI configuration")

def check_common_linkedin_errors():
    """Check for common LinkedIn API errors and solutions."""
    print("\n🚨 Common LinkedIn API Errors & Solutions")
    print("=" * 50)
    
    errors = {
        "invalid_client": "❌ Invalid Client ID or Secret",
        "invalid_redirect_uri": "❌ Redirect URI mismatch",
        "invalid_scope": "❌ Invalid scope requested",
        "access_denied": "❌ User denied permission",
        "server_error": "❌ LinkedIn server error",
        "invalid_grant": "❌ Invalid authorization code",
        "insufficient_scope": "❌ App doesn't have required permissions"
    }
    
    for error, description in errors.items():
        print(f"{description}")
        if error == "invalid_client":
            print("   Solution: Check your Client ID and Secret in config.py")
        elif error == "invalid_redirect_uri":
            print("   Solution: Ensure redirect URI matches exactly in LinkedIn app settings")
        elif error == "invalid_scope":
            print("   Solution: Use scope: 'r_liteprofile r_emailaddress w_member_social'")
        elif error == "access_denied":
            print("   Solution: User needs to grant permissions during OAuth flow")
        elif error == "insufficient_scope":
            print("   Solution: Request additional permissions in LinkedIn app dashboard")
        print()

def create_env_file_template():
    """Create a .env file template with correct LinkedIn configuration."""
    print("\n📝 .env File Template")
    print("=" * 50)
    
    env_content = f"""# Database Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=social_media_automation

# JWT Configuration
SECRET_KEY=my-super-secret-jwt-key-for-development-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LinkedIn OAuth Configuration
LINKEDIN_CLIENT_ID={settings.linkedin_client_id}
LINKEDIN_CLIENT_SECRET={settings.linkedin_client_secret}
LINKEDIN_REDIRECT_URI={settings.linkedin_redirect_uri}
LINKEDIN_SCOPE={settings.linkedin_scope}

# LinkedIn Tokens (will be filled automatically in database)
LINKEDIN_ACCESS_TOKEN=
LINKEDIN_REFRESH_TOKEN=

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=
EMAIL_PASSWORD=

# AI Configuration
GEMINI_API_KEY=

# Image Generation APIs
OPENAI_API_KEY=
UNSPLASH_ACCESS_KEY=

# Other Social Media API Keys
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
INSTAGRAM_USERNAME=
INSTAGRAM_PASSWORD=
"""
    
    print("Copy this content to your .env file:")
    print("-" * 30)
    print(env_content)
    print("-" * 30)
    
    # Try to create the .env file
    try:
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        with open(env_path, 'w') as f:
            f.write(env_content)
        print(f"✅ Created .env file at: {env_path}")
    except Exception as e:
        print(f"❌ Could not create .env file: {e}")
        print("Please create it manually with the content above")

def provide_troubleshooting_steps():
    """Provide step-by-step troubleshooting guide."""
    print("\n🔧 Step-by-Step Troubleshooting")
    print("=" * 50)
    
    steps = [
        "1. Check LinkedIn App Configuration:",
        "   - Go to https://developer.linkedin.com/",
        "   - Verify your app has the correct redirect URI",
        "   - Ensure you have 'Sign In with LinkedIn' product enabled",
        "",
        "2. Test the OAuth Flow:",
        "   - Use the auth URL generated above",
        "   - Complete the LinkedIn login",
        "   - Check if you get redirected properly",
        "",
        "3. Check Backend Logs:",
        "   - Look for detailed error messages in backend console",
        "   - Check if token exchange is successful",
        "   - Verify profile data retrieval",
        "",
        "4. Verify Environment Variables:",
        "   - Ensure .env file exists in backend directory",
        "   - Check that LinkedIn credentials are correct",
        "   - Restart the backend server after changes",
        "",
        "5. Test with Debug Script:",
        "   - Run: python debug_linkedin_api.py",
        "   - Follow the prompts to test each step",
        "",
        "6. Common Fixes:",
        "   - Clear browser cookies and cache",
        "   - Try incognito/private browsing mode",
        "   - Check if LinkedIn app is approved",
        "   - Verify redirect URI matches exactly"
    ]
    
    for step in steps:
        print(step)

def main():
    """Main function to run all checks and fixes."""
    print("🔧 LinkedIn API Issue Fixer")
    print("=" * 60)
    
    # Check configuration
    if not check_linkedin_app_configuration():
        print("\n❌ Configuration issues found. Please fix them first.")
        return
    
    # Generate auth URL
    auth_url = generate_linkedin_auth_url()
    
    # Test permissions
    test_linkedin_api_permissions()
    
    # Check common errors
    check_common_linkedin_errors()
    
    # Create .env template
    create_env_file_template()
    
    # Provide troubleshooting steps
    provide_troubleshooting_steps()
    
    print("\n" + "=" * 60)
    print("🎯 Next Steps:")
    print("1. Fix any configuration issues identified above")
    print("2. Test the OAuth flow using the auth URL")
    print("3. Check backend logs for detailed error messages")
    print("4. Run the debug script if issues persist")
    print("5. Contact LinkedIn support if app permissions are the issue")

if __name__ == "__main__":
    main() 