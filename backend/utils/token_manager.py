"""
LinkedIn OAuth Token Manager
Handles token validation, refresh, and management for LinkedIn API integration.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from bson import ObjectId

from database import get_database, PLATFORM_CONNECTIONS_COLLECTION
from utils.linkedin_service import linkedin_service

logger = logging.getLogger(__name__)


class LinkedInTokenManager:
    """Manages LinkedIn OAuth tokens for users."""
    
    @staticmethod
    async def get_valid_token(user_id: ObjectId) -> Optional[str]:
        """
        Get a valid LinkedIn access token for a user.
        Automatically refreshes the token if it's expired.
        
        Args:
            user_id: The user's ObjectId
            
        Returns:
            Valid access token or None if not available
        """
        try:
            db = get_database()
            
            # Get LinkedIn connection
            connection = await db[PLATFORM_CONNECTIONS_COLLECTION].find_one({
                "user_id": user_id,
                "platform": "linkedin",
                "is_connected": True
            })
            
            if not connection:
                logger.warning(f"No LinkedIn connection found for user {user_id}")
                return None
            
            access_token = connection.get("access_token")
            if not access_token:
                logger.warning(f"No access token found for user {user_id}")
                return None
            
            # Check if token is expired
            expires_at = connection.get("expires_at")
            if expires_at and isinstance(expires_at, str):
                expires_at = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
            
            # If token is expired or will expire soon (within 1 hour), refresh it
            if expires_at and expires_at <= datetime.utcnow() + timedelta(hours=1):
                logger.info(f"Token expired or expiring soon for user {user_id}, refreshing...")
                new_token = await LinkedInTokenManager._refresh_token(connection)
                if new_token:
                    return new_token
                else:
                    logger.error(f"Failed to refresh token for user {user_id}")
                    return None
            
            # Validate token
            is_valid = await linkedin_service.validate_token(access_token)
            if not is_valid:
                logger.info(f"Token validation failed for user {user_id}, attempting refresh...")
                new_token = await LinkedInTokenManager._refresh_token(connection)
                if new_token:
                    return new_token
                else:
                    logger.error(f"Failed to refresh invalid token for user {user_id}")
                    return None
            
            return access_token
            
        except Exception as e:
            logger.error(f"Error getting valid token for user {user_id}: {e}")
            return None
    
    @staticmethod
    async def _refresh_token(connection: Dict[str, Any]) -> Optional[str]:
        """
        Refresh a LinkedIn access token.
        
        Args:
            connection: The platform connection document
            
        Returns:
            New access token or None if refresh failed
        """
        try:
            refresh_token = connection.get("refresh_token")
            if not refresh_token:
                logger.error("No refresh token available")
                return None
            
            # Refresh the token
            token_data = await linkedin_service.refresh_access_token(refresh_token)
            if not token_data:
                logger.error("Failed to refresh access token")
                return None
            
            # Update the connection in database
            db = get_database()
            await db[PLATFORM_CONNECTIONS_COLLECTION].update_one(
                {"_id": connection["_id"]},
                {
                    "$set": {
                        "access_token": token_data["access_token"],
                        "refresh_token": token_data.get("refresh_token", refresh_token),
                        "expires_at": token_data["expires_at"],
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            logger.info(f"Successfully refreshed token for user {connection['user_id']}")
            return token_data["access_token"]
            
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return None
    
    @staticmethod
    async def validate_and_refresh_token(user_id: ObjectId) -> Optional[str]:
        """
        Validate and refresh token if needed. This is a convenience method
        that combines validation and refresh logic.
        
        Args:
            user_id: The user's ObjectId
            
        Returns:
            Valid access token or None if not available
        """
        return await LinkedInTokenManager.get_valid_token(user_id)
    
    @staticmethod
    async def store_token(user_id: ObjectId, token_data: Dict[str, Any]) -> bool:
        """
        Store a new LinkedIn token for a user.
        
        Args:
            user_id: The user's ObjectId
            token_data: Token data from LinkedIn OAuth
            
        Returns:
            True if stored successfully, False otherwise
        """
        try:
            db = get_database()
            
            connection_doc = {
                "user_id": user_id,
                "platform": "linkedin",
                "is_connected": True,
                "access_token": token_data["access_token"],
                "refresh_token": token_data.get("refresh_token"),
                "expires_at": token_data["expires_at"],
                "updated_at": datetime.utcnow()
            }
            
            # Upsert the connection
            result = await db[PLATFORM_CONNECTIONS_COLLECTION].replace_one(
                {
                    "user_id": user_id,
                    "platform": "linkedin"
                },
                connection_doc,
                upsert=True
            )
            
            logger.info(f"Successfully stored LinkedIn token for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing token for user {user_id}: {e}")
            return False
    
    @staticmethod
    async def revoke_token(user_id: ObjectId) -> bool:
        """
        Revoke/remove LinkedIn token for a user.
        
        Args:
            user_id: The user's ObjectId
            
        Returns:
            True if revoked successfully, False otherwise
        """
        try:
            db = get_database()
            
            result = await db[PLATFORM_CONNECTIONS_COLLECTION].update_one(
                {
                    "user_id": user_id,
                    "platform": "linkedin"
                },
                {
                    "$set": {
                        "is_connected": False,
                        "access_token": None,
                        "refresh_token": None,
                        "expires_at": None,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            logger.info(f"Successfully revoked LinkedIn token for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error revoking token for user {user_id}: {e}")
            return False
    
    @staticmethod
    async def get_token_info(user_id: ObjectId) -> Optional[Dict[str, Any]]:
        """
        Get token information for a user.
        
        Args:
            user_id: The user's ObjectId
            
        Returns:
            Token information or None if not found
        """
        try:
            db = get_database()
            
            connection = await db[PLATFORM_CONNECTIONS_COLLECTION].find_one({
                "user_id": user_id,
                "platform": "linkedin"
            })
            
            if not connection:
                return None
            
            return {
                "is_connected": connection.get("is_connected", False),
                "expires_at": connection.get("expires_at"),
                "platform_username": connection.get("platform_username"),
                "updated_at": connection.get("updated_at")
            }
            
        except Exception as e:
            logger.error(f"Error getting token info for user {user_id}: {e}")
            return None


# Global instance
linkedin_token_manager = LinkedInTokenManager() 