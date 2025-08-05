from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId
import logging

from database import get_database, USERS_COLLECTION
from models import UserUpdate, User
from utils import verify_token

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


@router.get("/profile", response_model=dict)
async def get_user_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user's profile."""
    try:
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        db = get_database()
        user = await db[USERS_COLLECTION].find_one({"email": email})
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Convert ObjectId to string and prepare user data
        user_data = {
            "_id": str(user["_id"]),
            "full_name": user.get("full_name", ""),
            "email": user.get("email", ""),
            "mobile_number": user.get("mobile_number", ""),
            "profession": user.get("profession", ""),
            "interests": user.get("interests", []),
            "custom_prompt": user.get("custom_prompt", ""),
            "role": user.get("role", "individual"),
            "company_name": user.get("company_name"),
            "website": user.get("website"),
            "industry": user.get("industry"),
            "is_verified": user.get("is_verified", False),
            "is_profile_complete": user.get("is_profile_complete", False),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at")
        }
        
        return user_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_user_profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/profile", response_model=User)
async def update_user_profile(
    user_update: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update current user's profile."""
    try:
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        db = get_database()
        
        # Remove None values from update data
        update_data = {k: v for k, v in user_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )
        
        # Add updated timestamp
        update_data["updated_at"] = "2024-01-01T00:00:00Z"
        
        # Update user
        result = await db[USERS_COLLECTION].update_one(
            {"email": email},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get updated user
        updated_user = await db[USERS_COLLECTION].find_one({"email": email})
        updated_user["_id"] = str(updated_user["_id"])
        
        return updated_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_user_profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/complete-profile", response_model=dict)
async def complete_user_profile(
    user_update: UserUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Complete user profile setup."""
    try:
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        db = get_database()
        
        # Validate required fields
        required_fields = ["full_name", "mobile_number", "destination", "interests", "custom_prompt"]
        update_data = user_update.dict()
        
        missing_fields = [field for field in required_fields if not update_data.get(field)]
        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Validate interests
        if len(update_data["interests"]) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least 5 interests are required"
            )
        
        # Update user and mark profile as complete
        update_data["is_profile_complete"] = True
        update_data["updated_at"] = "2024-01-01T00:00:00Z"
        
        result = await db[USERS_COLLECTION].update_one(
            {"email": email},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "message": "Profile completed successfully",
            "is_profile_complete": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in complete_user_profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/interests", response_model=dict)
async def get_available_interests():
    """Get list of available interests."""
    interests = [
        "Motivation",
        "Inspiration", 
        "Sports",
        "Education",
        "Travel and Adventure",
        "Business",
        "Health",
        "Fashion",
        "Technology",
        "Food and Cooking",
        "Fitness",
        "Art and Design",
        "Music",
        "Books and Reading",
        "Photography",
        "Gaming",
        "Pets and Animals",
        "Environment",
        "Science",
        "Others"
    ]
    
    return {"interests": interests}


@router.delete("/account", response_model=dict)
async def delete_user_account(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Delete user account."""
    try:
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        db = get_database()
        
        # Delete user
        result = await db[USERS_COLLECTION].delete_one({"email": email})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "Account deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_user_account: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 