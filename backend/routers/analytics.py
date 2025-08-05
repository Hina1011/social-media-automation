from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any
from bson import ObjectId
from datetime import datetime, timedelta
import logging

from database import get_database, USERS_COLLECTION, ANALYTICS_COLLECTION, POSTS_COLLECTION
from models import Analytics, AnalyticsCreate, AnalyticsSummary, AnalyticsRequest
from utils import verify_token

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get analytics summary for the current user."""
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
        
        # Get analytics data for the last 30 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        analytics_data = await db[ANALYTICS_COLLECTION].find({
            "user_id": ObjectId(user["_id"]),
            "date": {"$gte": start_date, "$lte": end_date}
        }).to_list(length=None)
        
        # Calculate summary
        total_followers = sum(data.get("followers_count", 0) for data in analytics_data)
        total_engagement = sum(
            data.get("likes_count", 0) + data.get("comments_count", 0) + data.get("shares_count", 0)
            for data in analytics_data
        )
        
        # Calculate average engagement rate
        engagement_rates = [data.get("engagement_rate", 0) for data in analytics_data if data.get("engagement_rate", 0) > 0]
        average_engagement_rate = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0
        
        # Platform breakdown
        platform_breakdown = {}
        platforms = ["instagram", "linkedin", "facebook", "twitter"]
        
        for platform in platforms:
            platform_data = [data for data in analytics_data if data.get("platform") == platform]
            if platform_data:
                platform_breakdown[platform] = {
                    "followers": sum(data.get("followers_count", 0) for data in platform_data),
                    "engagement": sum(
                        data.get("likes_count", 0) + data.get("comments_count", 0) + data.get("shares_count", 0)
                        for data in platform_data
                    ),
                    "posts": len(platform_data)
                }
            else:
                platform_breakdown[platform] = {
                    "followers": 0,
                    "engagement": 0,
                    "posts": 0
                }
        
        # Growth trend (last 7 days)
        growth_trend = []
        for i in range(7):
            date = end_date - timedelta(days=i)
            day_data = [data for data in analytics_data if data.get("date").date() == date.date()]
            
            if day_data:
                growth_trend.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "followers": sum(data.get("followers_count", 0) for data in day_data),
                    "engagement": sum(
                        data.get("likes_count", 0) + data.get("comments_count", 0) + data.get("shares_count", 0)
                        for data in day_data
                    )
                })
            else:
                growth_trend.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "followers": 0,
                    "engagement": 0
                })
        
        # Top posts (based on engagement)
        top_posts = await db[POSTS_COLLECTION].find({
            "user_id": ObjectId(user["_id"]),
            "status": "posted"
        }).sort("engagement_data.total_engagement", -1).limit(5).to_list(length=None)
        
        # Convert ObjectIds to strings
        for post in top_posts:
            post["_id"] = str(post["_id"])
            post["user_id"] = str(post["user_id"])
        
        return AnalyticsSummary(
            total_followers=total_followers,
            total_engagement=total_engagement,
            average_engagement_rate=average_engagement_rate,
            platform_breakdown=platform_breakdown,
            growth_trend=growth_trend,
            top_posts=top_posts
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_analytics_summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/platform/{platform}", response_model=List[Analytics])
async def get_platform_analytics(
    platform: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    days: int = 30
):
    """Get analytics for a specific platform."""
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
        
        # Validate platform
        valid_platforms = ["instagram", "linkedin", "facebook", "twitter"]
        if platform not in valid_platforms:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid platform"
            )
        
        # Get analytics data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        analytics_data = await db[ANALYTICS_COLLECTION].find({
            "user_id": ObjectId(user["_id"]),
            "platform": platform,
            "date": {"$gte": start_date, "$lte": end_date}
        }).sort("date", 1).to_list(length=None)
        
        # Convert ObjectIds to strings
        for data in analytics_data:
            data["_id"] = str(data["_id"])
            data["user_id"] = str(data["user_id"])
        
        return analytics_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_platform_analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/track", response_model=dict)
async def track_analytics(
    analytics_data: AnalyticsCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Track analytics data for a platform."""
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
        
        # Create analytics document
        analytics_doc = analytics_data.dict()
        analytics_doc["user_id"] = ObjectId(user["_id"])
        analytics_doc["created_at"] = "2024-01-01T00:00:00Z"
        analytics_doc["updated_at"] = "2024-01-01T00:00:00Z"
        
        # Insert analytics data
        result = await db[ANALYTICS_COLLECTION].insert_one(analytics_doc)
        
        return {
            "message": "Analytics data tracked successfully",
            "analytics_id": str(result.inserted_id)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in track_analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/growth", response_model=Dict[str, Any])
async def get_growth_analytics(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    days: int = 30
):
    """Get growth analytics data."""
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
        
        # Get analytics data
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        analytics_data = await db[ANALYTICS_COLLECTION].find({
            "user_id": ObjectId(user["_id"]),
            "date": {"$gte": start_date, "$lte": end_date}
        }).sort("date", 1).to_list(length=None)
        
        # Process growth data
        growth_data = {}
        platforms = ["instagram", "linkedin", "facebook", "twitter"]
        
        for platform in platforms:
            platform_data = [data for data in analytics_data if data.get("platform") == platform]
            
            if platform_data:
                # Calculate growth metrics
                followers_growth = []
                engagement_growth = []
                
                for data in platform_data:
                    followers_growth.append({
                        "date": data["date"].strftime("%Y-%m-%d"),
                        "followers": data.get("followers_count", 0)
                    })
                    
                    engagement_growth.append({
                        "date": data["date"].strftime("%Y-%m-%d"),
                        "engagement": data.get("likes_count", 0) + data.get("comments_count", 0) + data.get("shares_count", 0)
                    })
                
                growth_data[platform] = {
                    "followers_growth": followers_growth,
                    "engagement_growth": engagement_growth,
                    "total_followers": max(data.get("followers_count", 0) for data in platform_data),
                    "total_engagement": sum(
                        data.get("likes_count", 0) + data.get("comments_count", 0) + data.get("shares_count", 0)
                        for data in platform_data
                    )
                }
            else:
                growth_data[platform] = {
                    "followers_growth": [],
                    "engagement_growth": [],
                    "total_followers": 0,
                    "total_engagement": 0
                }
        
        return growth_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_growth_analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/posts-performance", response_model=List[Dict[str, Any]])
async def get_posts_performance(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    limit: int = 10
):
    """Get performance data for posts."""
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
        
        # Get posts with engagement data
        posts = await db[POSTS_COLLECTION].find({
            "user_id": ObjectId(user["_id"]),
            "status": "posted",
            "engagement_data": {"$exists": True}
        }).sort("engagement_data.total_engagement", -1).limit(limit).to_list(length=None)
        
        # Process posts data
        posts_performance = []
        for post in posts:
            engagement_data = post.get("engagement_data", {})
            posts_performance.append({
                "post_id": str(post["_id"]),
                "caption": post.get("caption", "")[:100] + "..." if len(post.get("caption", "")) > 100 else post.get("caption", ""),
                "platform": post.get("platforms", [""])[0],
                "posted_date": post.get("posted_at", ""),
                "likes": engagement_data.get("likes", 0),
                "comments": engagement_data.get("comments", 0),
                "shares": engagement_data.get("shares", 0),
                "total_engagement": engagement_data.get("total_engagement", 0),
                "engagement_rate": engagement_data.get("engagement_rate", 0)
            })
        
        return posts_performance
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_posts_performance: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 