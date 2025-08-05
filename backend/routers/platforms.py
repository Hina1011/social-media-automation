from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from bson import ObjectId
import logging
from datetime import datetime

from database import get_database, USERS_COLLECTION, PLATFORM_CONNECTIONS_COLLECTION
from models import (
    PlatformConnection, PlatformConnectionCreate, PlatformConnectionUpdate,
    PlatformAuthRequest, PlatformAuthResponse
)
from utils import verify_token
from utils.linkedin_service import linkedin_service
from utils.token_manager import linkedin_token_manager

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/platforms")
security = HTTPBearer()


@router.get("/", response_model=List[dict])
@router.get("", response_model=List[dict])
async def get_platform_connections(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get user's platform connections."""
    try:
        logger.info("Platform connections request received")
        token = credentials.credentials
        logger.info(f"Token received, length: {len(token) if token else 0}")
        
        email = verify_token(token)
        logger.info(f"Token verification result: {email}")
        
        if not email:
            logger.error("Invalid token for platform connections")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        db = get_database()
        
        # Get user
        user = await db[USERS_COLLECTION].find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get platform connections
        connections = await db[PLATFORM_CONNECTIONS_COLLECTION].find(
            {"user_id": ObjectId(user["_id"])}
        ).to_list(length=None)
        
        # Convert ObjectIds to strings and prepare connection data
        connection_list = []
        for connection in connections:
            connection_data = {
                "_id": str(connection["_id"]),
                "user_id": str(connection["user_id"]),
                "platform": connection.get("platform", ""),
                "is_connected": connection.get("is_connected", False),
                "platform_username": connection.get("platform_username"),
                "access_token": connection.get("access_token"),
                "refresh_token": connection.get("refresh_token"),
                "created_at": connection.get("created_at"),
                "updated_at": connection.get("updated_at")
            }
            connection_list.append(connection_data)
        
        return connection_list
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_platform_connections: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/linkedin/auth-url")
async def get_linkedin_auth_url(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get LinkedIn OAuth authorization URL."""
    try:
        logger.info("=== LinkedIn Auth URL Request ===")
        logger.info(f"Received credentials: {credentials}")
        
        token = credentials.credentials
        logger.info(f"Token length: {len(token) if token else 0}")
        
        email = verify_token(token)
        logger.info(f"Verified email: {email}")
        
        if not email:
            logger.error("Token verification failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Generate state parameter with user email
        state = f"linkedin_auth_{email}"
        logger.info(f"Generated state: {state}")
        
        auth_url = linkedin_service.get_auth_url(state)
        logger.info(f"Generated auth URL: {auth_url}")
        
        response_data = {
            "auth_url": auth_url,
            "state": state
        }
        logger.info(f"Returning response: {response_data}")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating LinkedIn auth URL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/linkedin/callback")
async def linkedin_oauth_callback(
    auth_request: PlatformAuthRequest
):
    """Handle LinkedIn OAuth callback."""
    try:
        logger.info("=== LinkedIn Callback Request ===")
        logger.info(f"Request data: {auth_request}")
        
        # Extract email from state parameter
        state = auth_request.state
        auth_code = auth_request.auth_code
        logger.info(f"State parameter: {state}")
        logger.info(f"Auth code (first 20 chars): {auth_code[:20] if auth_code else None}")
        
        if not state or not state.startswith("linkedin_auth_"):
            logger.error(f"Invalid state parameter: {state}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid state parameter"
            )
            
        if not auth_code:
            logger.error("No auth code provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authorization code is required"
            )
            
        email = state.replace("linkedin_auth_", "")
        logger.info(f"Extracted email: {email}")
        logger.info(f"Extracted email: {email}")

        if not auth_request.auth_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authorization code is required"
            )
        
        db = get_database()
        
        # Get the authenticated user
        user = await db[USERS_COLLECTION].find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Exchange code for token
        logger.info(f"Attempting to exchange code: {auth_request.auth_code[:20]}...")
        try:
            token_data = await linkedin_service.exchange_code_for_token(auth_request.auth_code)
            if not token_data:
                logger.error("Token exchange failed - no token data returned")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to exchange authorization code for token"
                )
            
            logger.info("Token exchange successful")
            logger.info(f"Access token (first 20 chars): {token_data['access_token'][:20]}...")
            
            # Get LinkedIn profile info
            try:
                profile_data = await linkedin_service.get_user_profile(token_data["access_token"])
                if not profile_data:
                    logger.error("Failed to get LinkedIn profile data - profile_data is None")
                    # Create a fallback profile data to prevent the connection from failing
                    logger.warning("Using fallback profile data")
                    profile_data = {
                        "id": "linkedin_user",
                        "first_name": "LinkedIn",
                        "last_name": "User"
                    }
                
                logger.info("Successfully retrieved profile data:")
                logger.info(profile_data)
                
            except Exception as e:
                logger.error(f"Error getting LinkedIn profile: {str(e)}")
                # Use fallback profile data instead of failing
                logger.warning("Using fallback profile data due to profile retrieval error")
                profile_data = {
                    "id": "linkedin_user",
                    "first_name": "LinkedIn", 
                    "last_name": "User"
                }
                
        except Exception as e:
            logger.error(f"Error during token exchange: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to exchange authorization code: {str(e)}"
            )
        
        # Store token and profile data
        platform_data = {
            "user_id": ObjectId(user["_id"]),
            "platform": "linkedin",
            "is_connected": True,
            "platform_username": f"{profile_data.get('first_name', '')} {profile_data.get('last_name', '')}".strip(),
            "access_token": token_data["access_token"],
            "refresh_token": token_data.get("refresh_token"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Update or insert platform connection
        await db[PLATFORM_CONNECTIONS_COLLECTION].update_one(
            {
                "user_id": ObjectId(user["_id"]),
                "platform": "linkedin"
            },
            {"$set": platform_data},
            upsert=True
        )
        
        # Store token in token manager
        await linkedin_token_manager.store_token(
            user_id=ObjectId(user["_id"]),
            token_data=token_data
        )
        
        return {
            "success": True,
            "message": "LinkedIn connected successfully",
            "platform": "linkedin",
            "is_connected": True,
            "username": platform_data["platform_username"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in LinkedIn callback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/status", response_model=dict)
async def get_platform_status(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get status of all platform connections."""
    try:
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        db = get_database()
        
        # Get user
        user = await db[USERS_COLLECTION].find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get all platform connections
        connections = await db[PLATFORM_CONNECTIONS_COLLECTION].find(
            {"user_id": ObjectId(user["_id"])}
        ).to_list(length=None)
        
        status = {
            "linkedin": False,
            "facebook": False,
            "twitter": False,
            "instagram": False
        }
        
        for connection in connections:
            if connection.get("is_connected"):
                status[connection["platform"]] = True
        
        return status
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_platform_status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/disconnect/{platform}", response_model=dict)
async def disconnect_platform(
    platform: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Disconnect a social media platform."""
    try:
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        db = get_database()
        
        # Get user
        user = await db[USERS_COLLECTION].find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update connection status
        result = await db[PLATFORM_CONNECTIONS_COLLECTION].update_one(
            {
                "user_id": ObjectId(user["_id"]),
                "platform": platform
            },
            {
                "$set": {
                    "is_connected": False,
                    "access_token": None,
                    "refresh_token": None,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Also revoke token in token manager for LinkedIn
        if platform == "linkedin":
            try:
                await linkedin_token_manager.revoke_token(ObjectId(user["_id"]))
            except Exception as e:
                logger.error(f"Error revoking LinkedIn token: {e}")
                # Don't fail if token revocation fails
                pass
        
        return {"message": f"Disconnected from {platform} successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in disconnect_platform: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )