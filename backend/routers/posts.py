from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from bson import ObjectId
import logging

from database import get_database, USERS_COLLECTION, POSTS_COLLECTION, PLATFORM_CONNECTIONS_COLLECTION
from models import (
    PostCreate, PostUpdate, Post, PostGenerationRequest, 
    PostApprovalRequest, PostBatch
)
from utils import verify_token, ai_generator
from utils.linkedin_service import linkedin_service
from utils.token_manager import linkedin_token_manager

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


@router.post("/generate", response_model=List[dict])
async def generate_posts(
    request: PostGenerationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate 7 days of social media posts using AI."""
    try:
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        db = get_database()
        
        # Get user data
        user = await db[USERS_COLLECTION].find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if profile is complete
        if not user.get("is_profile_complete", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please complete your profile first"
            )
        
        # Generate posts using AI
        generated_posts = await ai_generator.generate_7_day_batch(
            interests=user["interests"],
            custom_prompt=request.custom_prompt,
            platforms=request.platforms,
            start_date=request.start_date
        )
        
        # Create post documents
        posts_to_insert = []
        for post_data in generated_posts:
            post_doc = {
                "user_id": ObjectId(user["_id"]),
                "caption": post_data["caption"],
                "hashtags": post_data["hashtags"],
                "scheduled_date": post_data["scheduled_date"],
                "platforms": [post_data["platform"]],
                "status": "draft",
                "custom_prompt": request.custom_prompt,
                "image_prompt": post_data["image_prompt"],
                "image_url": post_data.get("image_url"),
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
            posts_to_insert.append(post_doc)
        
        # Insert posts
        if posts_to_insert:
            result = await db[POSTS_COLLECTION].insert_many(posts_to_insert)
            
            # Get inserted posts
            inserted_posts = await db[POSTS_COLLECTION].find(
                {"_id": {"$in": result.inserted_ids}}
            ).to_list(length=None)
            
            # Convert ObjectIds to strings and prepare post data
            post_list = []
            for post in inserted_posts:
                post_data = {
                    "_id": str(post["_id"]),
                    "user_id": str(post["user_id"]),
                    "caption": post.get("caption", ""),
                    "hashtags": post.get("hashtags", []),
                    "image_url": post.get("image_url"),
                    "scheduled_date": post.get("scheduled_date"),
                    "platforms": post.get("platforms", []),
                    "status": post.get("status", "draft"),
                    "custom_prompt": post.get("custom_prompt"),
                    "image_prompt": post.get("image_prompt"),
                    "created_at": post.get("created_at"),
                    "updated_at": post.get("updated_at"),
                    "posted_at": post.get("posted_at"),
                    "engagement_data": post.get("engagement_data")
                }
                post_list.append(post_data)
            
            return post_list
        
        return []
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate_posts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=List[dict])
async def get_user_posts(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    status_filter: str = None,
    platform: str = None
):
    """Get user's posts with optional filtering."""
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
        
        # Build query
        query = {"user_id": ObjectId(user["_id"])}
        
        if status_filter:
            query["status"] = status_filter
        
        if platform:
            query["platforms"] = platform
        
        # Get posts
        posts = await db[POSTS_COLLECTION].find(query).sort("scheduled_date", 1).to_list(length=None)
        
        # Convert ObjectIds to strings and prepare post data
        post_list = []
        for post in posts:
            post_data = {
                "_id": str(post["_id"]),
                "user_id": str(post["user_id"]),
                "caption": post.get("caption", ""),
                "hashtags": post.get("hashtags", []),
                "image_url": post.get("image_url"),
                "scheduled_date": post.get("scheduled_date"),
                "platforms": post.get("platforms", []),
                "status": post.get("status", "draft"),
                "custom_prompt": post.get("custom_prompt"),
                "image_prompt": post.get("image_prompt"),
                "created_at": post.get("created_at"),
                "updated_at": post.get("updated_at"),
                "posted_at": post.get("posted_at"),
                "engagement_data": post.get("engagement_data")
            }
            post_list.append(post_data)
        
        return post_list
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_user_posts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{post_id}", response_model=dict)
async def get_post(
    post_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific post by ID."""
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
        
        # Get post
        post = await db[POSTS_COLLECTION].find_one({
            "_id": ObjectId(post_id),
            "user_id": ObjectId(user["_id"])
        })
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Convert ObjectIds to strings and prepare post data
        post_data = {
            "_id": str(post["_id"]),
            "user_id": str(post["user_id"]),
            "caption": post.get("caption", ""),
            "hashtags": post.get("hashtags", []),
            "image_url": post.get("image_url"),
            "scheduled_date": post.get("scheduled_date"),
            "platforms": post.get("platforms", []),
            "status": post.get("status", "draft"),
            "custom_prompt": post.get("custom_prompt"),
            "image_prompt": post.get("image_prompt"),
            "created_at": post.get("created_at"),
            "updated_at": post.get("updated_at"),
            "posted_at": post.get("posted_at"),
            "engagement_data": post.get("engagement_data")
        }
        
        return post_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{post_id}", response_model=dict)
async def update_post(
    post_id: str,
    post_update: PostUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update a specific post."""
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
        
        # Remove None values from update data
        update_data = {k: v for k, v in post_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )
        
        # Add updated timestamp
        update_data["updated_at"] = "2024-01-01T00:00:00Z"
        
        # Update post
        result = await db[POSTS_COLLECTION].update_one(
            {
                "_id": ObjectId(post_id),
                "user_id": ObjectId(user["_id"])
            },
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Get updated post
        updated_post = await db[POSTS_COLLECTION].find_one({"_id": ObjectId(post_id)})
        
        # Convert ObjectIds to strings and prepare post data
        post_data = {
            "_id": str(updated_post["_id"]),
            "user_id": str(updated_post["user_id"]),
            "caption": updated_post.get("caption", ""),
            "hashtags": updated_post.get("hashtags", []),
            "image_url": updated_post.get("image_url"),
            "scheduled_date": updated_post.get("scheduled_date"),
            "platforms": updated_post.get("platforms", []),
            "status": updated_post.get("status", "draft"),
            "custom_prompt": updated_post.get("custom_prompt"),
            "image_prompt": updated_post.get("image_prompt"),
            "created_at": updated_post.get("created_at"),
            "updated_at": updated_post.get("updated_at"),
            "posted_at": updated_post.get("posted_at"),
            "engagement_data": updated_post.get("engagement_data")
        }
        
        return post_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/approve", response_model=dict)
async def approve_posts(
    approval_request: PostApprovalRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Approve posts for scheduling."""
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
        
        if approval_request.approve_all:
            # Approve all user's draft posts
            result = await db[POSTS_COLLECTION].update_many(
                {
                    "user_id": ObjectId(user["_id"]),
                    "status": "draft"
                },
                {
                    "$set": {
                        "status": "approved",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                }
            )
            
            return {
                "message": f"Approved {result.modified_count} posts",
                "approved_count": result.modified_count
            }
        else:
            # Approve specific posts
            post_ids = [ObjectId(pid) for pid in approval_request.post_ids]
            
            result = await db[POSTS_COLLECTION].update_many(
                {
                    "_id": {"$in": post_ids},
                    "user_id": ObjectId(user["_id"])
                },
                {
                    "$set": {
                        "status": "approved",
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                }
            )
            
            return {
                "message": f"Approved {result.modified_count} posts",
                "approved_count": result.modified_count
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in approve_posts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{post_id}", response_model=dict)
async def delete_post(
    post_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Delete a specific post."""
    try:
        logger.info(f"Delete request for post_id: {post_id}")
        
        token = credentials.credentials
        email = verify_token(token)
        if not email:
            logger.error(f"Invalid token for delete request")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        logger.info(f"Token verified for email: {email}")
        
        db = get_database()
        
        # Get user
        user = await db[USERS_COLLECTION].find_one({"email": email})
        if not user:
            logger.error(f"User not found for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        logger.info(f"User found: {user['_id']}")
        
        # Check if post exists first
        existing_post = await db[POSTS_COLLECTION].find_one({
            "_id": ObjectId(post_id),
            "user_id": ObjectId(user["_id"])
        })
        
        if not existing_post:
            logger.error(f"Post not found: {post_id} for user: {user['_id']}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        logger.info(f"Post found, proceeding with deletion")
        
        # Delete post
        result = await db[POSTS_COLLECTION].delete_one({
            "_id": ObjectId(post_id),
            "user_id": ObjectId(user["_id"])
        })
        
        if result.deleted_count == 0:
            logger.error(f"Delete operation failed for post: {post_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        logger.info(f"Post deleted successfully: {post_id}")
        return {"message": "Post deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/{post_id}/regenerate", response_model=dict)
async def regenerate_post(
    post_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Regenerate content for a specific post using AI."""
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
        
        # Get existing post
        post = await db[POSTS_COLLECTION].find_one({
            "_id": ObjectId(post_id),
            "user_id": ObjectId(user["_id"])
        })
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Generate new content using AI
        new_content = await ai_generator.generate_single_post(
            interests=user["interests"],
            platform=post["platforms"][0] if post["platforms"] else "instagram",
            custom_prompt=post.get("custom_prompt", "Create engaging social media content"),
            scheduled_date=post["scheduled_date"]
        )
        
        # Update post with new content
        update_data = {
            "caption": new_content["caption"],
            "hashtags": new_content["hashtags"],
            "image_prompt": new_content["image_prompt"],
            "image_url": new_content.get("image_url"),
            "updated_at": "2024-01-01T00:00:00Z"
        }
        
        result = await db[POSTS_COLLECTION].update_one(
            {"_id": ObjectId(post_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update post"
            )
        
        # Get updated post
        updated_post = await db[POSTS_COLLECTION].find_one({"_id": ObjectId(post_id)})
        
        # Convert ObjectIds to strings and prepare post data
        post_data = {
            "_id": str(updated_post["_id"]),
            "user_id": str(updated_post["user_id"]),
            "caption": updated_post.get("caption", ""),
            "hashtags": updated_post.get("hashtags", []),
            "image_url": updated_post.get("image_url"),
            "scheduled_date": updated_post.get("scheduled_date"),
            "platforms": updated_post.get("platforms", []),
            "status": updated_post.get("status", "draft"),
            "custom_prompt": updated_post.get("custom_prompt"),
            "image_prompt": updated_post.get("image_prompt"),
            "created_at": updated_post.get("created_at"),
            "updated_at": updated_post.get("updated_at"),
            "posted_at": updated_post.get("posted_at"),
            "engagement_data": updated_post.get("engagement_data")
        }
        
        return post_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in regenerate_post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/{post_id}/upload-image", response_model=dict)
async def upload_post_image(
    post_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Upload a custom image for a specific post."""
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
        
        # Get existing post
        post = await db[POSTS_COLLECTION].find_one({
            "_id": ObjectId(post_id),
            "user_id": ObjectId(user["_id"])
        })
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # For now, we'll return success - actual image upload would be implemented here
        # In a real implementation, you would:
        # 1. Save the uploaded image to storage
        # 2. Update the post with the new image URL
        # 3. Return the updated post data
        
        return {
            "message": "Image upload endpoint ready",
            "post_id": post_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_post_image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 


@router.post("/{post_id}/post-to-linkedin", response_model=dict)
async def post_to_linkedin(
    post_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Post a specific post to LinkedIn."""
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
        
        # Get the post
        try:
            post = await db[POSTS_COLLECTION].find_one({
                "_id": ObjectId(post_id),
                "user_id": ObjectId(user["_id"])
            })
        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Check if LinkedIn is connected
        linkedin_connection = await db[PLATFORM_CONNECTIONS_COLLECTION].find_one({
            "user_id": ObjectId(user["_id"]),
            "platform": "linkedin",
            "is_connected": True
        })
        
        if not linkedin_connection:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="LinkedIn account not connected. Please connect your LinkedIn account first."
            )
        
        # Prepare content for LinkedIn
        caption = post.get("caption", "")
        hashtags = post.get("hashtags", [])
        image_url = post.get("image_url")
        
        # Combine caption and hashtags
        content = caption
        if hashtags:
            content += "\n\n" + " ".join(hashtags)
        
        # Get valid access token using token manager
        access_token = await linkedin_token_manager.get_valid_token(ObjectId(user["_id"]))
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="LinkedIn access token not available or invalid. Please reconnect your LinkedIn account."
            )
        
        # Create post on LinkedIn
        result = await linkedin_service.create_post(access_token, content, image_url)
        
        if result and result.get("success"):
            # Update post status to indicate it was posted
            await db[POSTS_COLLECTION].update_one(
                {"_id": ObjectId(post_id)},
                {
                    "$set": {
                        "status": "posted",
                        "posted_to_linkedin": True,
                        "linkedin_post_id": result.get("post_id"),
                        "updated_at": "2024-01-01T00:00:00Z"
                    }
                }
            )
            
            return {
                "success": True,
                "message": "Post successfully shared on LinkedIn",
                "linkedin_post_id": result.get("post_id")
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("message", "Failed to post to LinkedIn") if result else "Failed to post to LinkedIn"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error posting to LinkedIn: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/batch-post-to-linkedin", response_model=dict)
async def batch_post_to_linkedin(
    post_ids: List[str],
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Post multiple posts to LinkedIn."""
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
        
        # Check if LinkedIn is connected
        linkedin_connection = await db[PLATFORM_CONNECTIONS_COLLECTION].find_one({
            "user_id": ObjectId(user["_id"]),
            "platform": "linkedin",
            "is_connected": True
        })
        
        if not linkedin_connection:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="LinkedIn account not connected. Please connect your LinkedIn account first."
            )
        
        # Get valid access token using token manager
        access_token = await linkedin_token_manager.get_valid_token(ObjectId(user["_id"]))
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="LinkedIn access token not available or invalid. Please reconnect your LinkedIn account."
            )
        
        # Get posts
        try:
            post_object_ids = [ObjectId(pid) for pid in post_ids]
            posts = await db[POSTS_COLLECTION].find({
                "_id": {"$in": post_object_ids},
                "user_id": ObjectId(user["_id"])
            }).to_list(length=None)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid post IDs"
            )
        
        if len(posts) != len(post_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some posts not found"
            )
        
        # Post each post to LinkedIn
        results = []
        for post in posts:
            caption = post.get("caption", "")
            hashtags = post.get("hashtags", [])
            image_url = post.get("image_url")
            
            content = caption
            if hashtags:
                content += "\n\n" + " ".join(hashtags)
            
            result = await linkedin_service.create_post(access_token, content, image_url)
            
            if result and result.get("success"):
                # Update post status
                await db[POSTS_COLLECTION].update_one(
                    {"_id": post["_id"]},
                    {
                        "$set": {
                            "status": "posted",
                            "posted_to_linkedin": True,
                            "linkedin_post_id": result.get("post_id"),
                            "updated_at": "2024-01-01T00:00:00Z"
                        }
                    }
                )
                
                results.append({
                    "post_id": str(post["_id"]),
                    "success": True,
                    "linkedin_post_id": result.get("post_id")
                })
            else:
                results.append({
                    "post_id": str(post["_id"]),
                    "success": False,
                    "error": result.get("message", "Failed to post") if result else "Failed to post"
                })
        
        success_count = sum(1 for r in results if r["success"])
        
        return {
            "success": True,
            "message": f"Posted {success_count} out of {len(posts)} posts to LinkedIn",
            "results": results,
            "total_posts": len(posts),
            "successful_posts": success_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch posting to LinkedIn: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 