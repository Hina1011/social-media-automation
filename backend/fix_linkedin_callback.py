from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId
import logging

from database import get_database, USERS_COLLECTION, PLATFORM_CONNECTIONS_COLLECTION
from models import PlatformAuthRequest
from utils import verify_token
from utils.linkedin_service import linkedin_service
from utils.token_manager import linkedin_token_manager

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

@router.post("/linkedin/callback")
async def linkedin_oauth_callback(
    auth_request: PlatformAuthRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Handle LinkedIn OAuth callback."""
    try:
        # Verify user token
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        if not auth_request.auth_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authorization code is required"
            )
        
        db = get_database()
        
        # Get authenticated user
        user = await db[USERS_COLLECTION].find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Exchange code for token
        logger.info(f"Attempting to exchange code: {auth_request.auth_code[:20]}...")
        token_data = await linkedin_service.exchange_code_for_token(auth_request.auth_code)
        if not token_data:
            logger.error("Token exchange failed - no token data returned")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to exchange authorization code for token"
            )
        
        logger.info("Token exchange successful")
        
        # Get LinkedIn profile info
        profile_data = await linkedin_service.get_user_profile(token_data["access_token"])
        if not profile_data:
            logger.error("Failed to get LinkedIn profile data")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get LinkedIn profile data"
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
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            expires_at=token_data.get("expires_at")
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