import requests
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

# Import from the config package that's actually being used
from config import settings

logger = logging.getLogger(__name__)


class LinkedInService:
    """LinkedIn API service for OAuth and posting."""
    
    def __init__(self):
        self.client_id = settings.linkedin_client_id
        self.client_secret = settings.linkedin_client_secret
        self.redirect_uri = settings.linkedin_redirect_uri
        self.scope = settings.linkedin_scope
        self.base_url = "https://api.linkedin.com/v2"
        self.auth_url = "https://www.linkedin.com/oauth/v2"
    
    def get_auth_url(self, state: str = None) -> str:
        """Generate LinkedIn OAuth authorization URL."""
        logger.info("Generating LinkedIn auth URL with params:")
        logger.info(f"- Client ID: {self.client_id}")
        logger.info(f"- Redirect URI: {self.redirect_uri}")
        logger.info(f"- Scope: {self.scope}")
        logger.info(f"- State: {state}")
        
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "state": state or "linkedin_auth"
        }
        
        from urllib.parse import urlencode
        query_string = urlencode(params)
        auth_url = f"{self.auth_url}/authorization?{query_string}"
        logger.info(f"Generated auth URL: {auth_url}")
        return auth_url
    
    async def exchange_code_for_token(self, auth_code: str) -> Optional[Dict[str, Any]]:
        """Exchange authorization code for access token."""
        try:
            token_url = f"{self.auth_url}/accessToken"
            
            # Log request details for debugging
            logger.info("=== Starting LinkedIn Token Exchange ===")
            logger.info(f"Token URL: {token_url}")
            logger.info(f"Client ID: {self.client_id}")
            logger.info(f"Redirect URI: {self.redirect_uri}")
            logger.info(f"Auth Code (first 20 chars): {auth_code[:20]}...")
            
            # Prepare data
            data = {
                "grant_type": "authorization_code",
                "code": auth_code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri
            }
            
            # Add headers
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            
            logger.info("=== Request Details ===")
            logger.info(f"Headers: {headers}")
            logger.info("Data:")
            for key, value in data.items():
                if key == 'code':
                    logger.info(f"  {key}: {value[:20]}...")
                elif key == 'client_secret':
                    logger.info(f"  {key}: [REDACTED]")
                else:
                    logger.info(f"  {key}: {value}")
            
            # Make the request
            response = requests.post(token_url, data=data, headers=headers)
            
            # Log response details
            logger.info("=== Response Details ===")
            logger.info(f"Status Code: {response.status_code}")
            logger.info(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                logger.error("Token Exchange Failed!")
                logger.error(f"Status Code: {response.status_code}")
                logger.error(f"Response Body: {response.text}")
                try:
                    error_json = response.json()
                    logger.error(f"Error Details: {error_json}")
                except:
                    logger.error("Could not parse error response as JSON")
                return None
            
            token_data = response.json()
            logger.info("Successfully exchanged code for LinkedIn token")
            
            if not token_data.get("access_token"):
                logger.error("No access token in response")
                logger.error(f"Response data: {token_data}")
                return None
            
            return {
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in"),
                "expires_at": datetime.utcnow() + timedelta(seconds=token_data.get("expires_in", 3600))
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error exchanging LinkedIn code for token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
                logger.error(f"Response headers: {dict(e.response.headers)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in token exchange: {e}")
            return None
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh LinkedIn access token."""
        try:
            token_url = f"{self.auth_url}/accessToken"
            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            
            response = requests.post(token_url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            logger.info("Successfully refreshed LinkedIn token")
            
            return {
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in"),
                "expires_at": datetime.utcnow() + timedelta(seconds=token_data.get("expires_in", 3600))
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error refreshing LinkedIn token: {e}")
            return None
    
    async def get_user_profile(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get LinkedIn user profile information."""
        try:
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            # Get basic profile - try both v2 and v2/me endpoints
            profile_url = f"{self.base_url}/me"
            logger.info(f"Requesting profile from URL: {profile_url}")
            
            # Make the request
            response = requests.get(profile_url, headers=headers)
            
            # If v2/me fails, try alternative endpoint
            if response.status_code != 200:
                logger.warning(f"v2/me failed with status {response.status_code}, trying alternative endpoint")
                profile_url = "https://api.linkedin.com/v2/me?projection=(id,localizedFirstName,localizedLastName)"
                response = requests.get(profile_url, headers=headers)
            
            # Log the response details
            logger.info(f"Profile request status code: {response.status_code}")
            logger.info(f"Profile response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                logger.error(f"Profile request failed. Status: {response.status_code}")
                logger.error(f"Response body: {response.text}")
                return None
            
            profile_data = response.json()
            logger.info(f"Profile data received: {profile_data}")
            
            # Log the full profile data for debugging
            logger.info("Raw profile data received:")
            logger.info(profile_data)
            
            # Extract profile info with fallbacks
            profile_info = {
                "id": profile_data.get("id", ""),
                "first_name": profile_data.get("localizedFirstName", profile_data.get("firstName", "LinkedIn")),
                "last_name": profile_data.get("localizedLastName", profile_data.get("lastName", "User"))
            }
            
            logger.info("Extracted profile info:")
            logger.info(profile_info)
            
            # Ensure we have at least an ID
            if not profile_info["id"]:
                logger.error("No profile ID found in response")
                # Try to extract ID from different possible locations
                if "id" in profile_data:
                    profile_info["id"] = profile_data["id"]
                elif "sub" in profile_data:  # OpenID Connect format
                    profile_info["id"] = profile_data["sub"]
                else:
                    logger.error("Could not find profile ID in any expected location")
                    return None
                
            return profile_info
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting LinkedIn profile: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
                logger.error(f"Response headers: {dict(e.response.headers)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting profile: {e}")
            return None
    
    async def validate_token(self, access_token: str) -> bool:
        """Validate if the access token is still valid."""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            response = requests.get(f"{self.base_url}/me", headers=headers)
            return response.status_code == 200
            
        except requests.exceptions.RequestException:
            return False


# Global instance
linkedin_service = LinkedInService()