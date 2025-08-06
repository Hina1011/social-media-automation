from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta
from bson import ObjectId
import logging

from database import get_database, USERS_COLLECTION, OTP_COLLECTION, is_database_connected
from models import UserCreate, UserLogin, OTPRequest, OTPVerify, Token, User
from utils import (
    get_password_hash, verify_password, create_access_token,
    generate_otp, send_otp_email, send_welcome_email
)
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


@router.get("/test")
async def test_auth_router():
    """Test endpoint to verify auth router is working."""
    return {"message": "Auth router is working!"}


@router.get("/debug")
async def debug_auth():
    """Debug endpoint to check database connection and settings."""
    try:
        # Check database connection
        db_connected = is_database_connected()
        if db_connected:
            try:
                from database import db
                await db.client.admin.command('ping')
                db_status = "connected"
            except Exception as e:
                db_status = f"error: {str(e)}"
        else:
            db_status = "not connected"
        
        # Check settings
        settings_info = {
            "secret_key": "***" if settings.JWT_SECRET_KEY else "NOT_SET",
            "algorithm": settings.JWT_ALGORITHM,
            "access_token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            "mongodb_url": settings.MONGODB_URL[:20] + "..." if len(settings.MONGODB_URL) > 20 else settings.MONGODB_URL,
            "database_name": settings.DATABASE_NAME
        }
        
        return {
            "message": "Debug info",
            "database": db_status,
            "database_connected": db_connected,
            "settings": settings_info
        }
    except Exception as e:
        return {"error": str(e)}


@router.post("/signup", response_model=dict)
async def signup(user_data: UserCreate):
    """User registration endpoint."""
    try:
        # Check database connection first
        if not is_database_connected():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service unavailable. Please check your MongoDB connection."
            )
        
        db = get_database()
        
        # Check if user already exists
        existing_user = await db[USERS_COLLECTION].find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user document
        user_doc = user_data.dict()
        user_doc["hashed_password"] = hashed_password
        user_doc["password"] = None  # Remove plain password
        user_doc["is_verified"] = True  # Auto-verify for development
        user_doc["is_profile_complete"] = True  # Auto-complete profile
        
        # Insert user
        result = await db[USERS_COLLECTION].insert_one(user_doc)
        
        # Auto-generate 7 posts for the new user (only if AI is configured)
        post_ids = []
        try:
            from utils import ai_generator
            from database import POSTS_COLLECTION
            from datetime import datetime, timedelta
            
            # Only generate posts for individual users
            if user_data.role == 'individual':
                logger.info(f"Auto-generating 7 days of posts for new user: {user_data.email}")
                
                # Generate 7 days of posts starting from tomorrow
                start_date = datetime.now() + timedelta(days=1)
                generated_posts = await ai_generator.generate_7_day_batch(
                    interests=user_data.interests,
                    custom_prompt=user_data.custom_prompt,
                    platforms=['instagram', 'linkedin', 'facebook', 'twitter'],  # Default platforms
                    start_date=start_date
                )
                
                # Create post documents
                posts_to_insert = []
                for post_data in generated_posts:
                    post_doc = {
                        "user_id": result.inserted_id,
                        "caption": post_data["caption"],
                        "hashtags": post_data["hashtags"],
                        "scheduled_date": post_data["scheduled_date"],
                        "platforms": post_data.get("platforms", ["instagram"]),
                        "status": "pending_approval",  # New status for approval workflow
                        "custom_prompt": user_data.custom_prompt,
                        "image_prompt": post_data["image_prompt"],
                        "image_url": post_data.get("image_url"),
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat(),
                        "batch_id": f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "is_auto_generated": True
                    }
                    posts_to_insert.append(post_doc)
                
                # Insert posts
                if posts_to_insert:
                    posts_result = await db[POSTS_COLLECTION].insert_many(posts_to_insert)
                    post_ids = [str(post_id) for post_id in posts_result.inserted_ids]
                    logger.info(f"Generated {len(post_ids)} posts for user {user_data.email}")
                
        except Exception as e:
            logger.error(f"Error auto-generating posts for user {user_data.email}: {e}")
            # Don't fail signup if post generation fails
        
        # Send welcome email
        try:
            await send_welcome_email(user_data.email, user_data.full_name)
        except Exception as e:
            logger.error(f"Error sending welcome email: {e}")
        
        return {
            "message": "User created successfully",
            "user_id": str(result.inserted_id),
            "auto_generated_posts": len(post_ids),
            "posts_ready_for_approval": len(post_ids) > 0
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in signup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """User login endpoint."""
    try:
        # Check database connection first
        if not is_database_connected():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service unavailable. Please check your MongoDB connection."
            )
        
        # Get database connection
        try:
            db = get_database()
        except Exception as db_error:
            logger.error(f"Database connection error in login: {db_error}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service unavailable"
            )
        
        # Find user
        user = await db[USERS_COLLECTION].find_one({"email": user_credentials.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        if not verify_password(user_credentials.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Check if user is verified (commented out for development)
        # if not user.get("is_verified", False):
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="Please verify your email first"
        #     )
        
        # Create access token
        try:
            access_token = create_access_token(
                data={"sub": user["email"]},
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
        except Exception as token_error:
            logger.error(f"Token creation error in login: {token_error}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create access token"
            )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/request-otp", response_model=dict)
async def request_otp(otp_request: OTPRequest):
    """Request OTP for email verification."""
    try:
        # Check database connection first
        if not is_database_connected():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service unavailable. Please check your MongoDB connection."
            )
        
        db = get_database()
        
        # Check if user exists
        user = await db[USERS_COLLECTION].find_one({"email": otp_request.email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate new OTP
        otp = generate_otp()
        
        # Update or create OTP record
        otp_doc = {
            "email": otp_request.email,
            "otp": otp,
            "created_at": "2024-01-01T00:00:00Z",
            "expires_at": "2024-01-01T00:00:00Z"
        }
        
        await db[OTP_COLLECTION].replace_one(
            {"email": otp_request.email},
            otp_doc,
            upsert=True
        )
        
        # Send OTP email
        email_sent = await send_otp_email(otp_request.email, otp)
        
        return {
            "message": "OTP sent successfully",
            "email_sent": email_sent
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in request_otp: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/verify-otp", response_model=dict)
async def verify_otp(otp_verify: OTPVerify):
    """Verify OTP and activate user account."""
    try:
        # Check database connection first
        if not is_database_connected():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service unavailable. Please check your MongoDB connection."
            )
        
        db = get_database()
        
        # Find OTP record
        otp_record = await db[OTP_COLLECTION].find_one({
            "email": otp_verify.email,
            "otp": otp_verify.otp
        })
        
        if not otp_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP"
            )
        
        # Check if OTP is expired (10 minutes)
        # In production, you'd check the actual timestamp
        
        # Update user as verified
        result = await db[USERS_COLLECTION].update_one(
            {"email": otp_verify.email},
            {"$set": {"is_verified": True}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get user data for welcome email
        user = await db[USERS_COLLECTION].find_one({"email": otp_verify.email})
        
        # Send welcome email
        await send_welcome_email(otp_verify.email, user["full_name"])
        
        # Delete OTP record
        await db[OTP_COLLECTION].delete_one({"email": otp_verify.email})
        
        return {
            "message": "Email verified successfully. Welcome to Social Media Automation!"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in verify_otp: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/me", response_model=dict)
async def get_current_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user information."""
    try:
        from utils import verify_token
        
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Check database connection first
        if not is_database_connected():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service unavailable. Please check your MongoDB connection."
            )
        
        try:
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
        except Exception as db_error:
            logger.error(f"Database error in get_current_user_info: {db_error}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service unavailable"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_current_user_info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 