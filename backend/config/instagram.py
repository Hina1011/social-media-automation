"""
Instagram OAuth Configuration
"""

# Instagram OAuth Configuration
# Replace these with your actual Instagram App credentials
# You can get these from https://developers.facebook.com/apps/

INSTAGRAM_CLIENT_ID = "your_instagram_client_id"
INSTAGRAM_CLIENT_SECRET = "your_instagram_client_secret"
INSTAGRAM_REDIRECT_URI = "http://localhost:3000/auth/instagram/callback"

# Instagram API endpoints
INSTAGRAM_AUTH_URL = "https://api.instagram.com/oauth/authorize"
INSTAGRAM_TOKEN_URL = "https://api.instagram.com/oauth/access_token"
INSTAGRAM_USER_INFO_URL = "https://graph.instagram.com/me"

# Instagram API scopes
INSTAGRAM_SCOPES = [
    "user_profile",
    "user_media"
]

def get_instagram_auth_url():
    """Generate Instagram OAuth authorization URL."""
    scopes = ",".join(INSTAGRAM_SCOPES)
    
    auth_url = (
        f"{INSTAGRAM_AUTH_URL}?"
        f"client_id={INSTAGRAM_CLIENT_ID}&"
        f"redirect_uri={INSTAGRAM_REDIRECT_URI}&"
        f"scope={scopes}&"
        f"response_type=code"
    )
    
    return auth_url 