import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from database import get_database, POSTS_COLLECTION, USERS_COLLECTION
from utils.linkedin_service import linkedin_service
from utils.token_manager import linkedin_token_manager

logger = logging.getLogger(__name__)

class PostScheduler:
    def __init__(self):
        self.is_running = False
        self.check_interval = 60  # Check every 60 seconds
        
    async def start(self):
        """Start the scheduler service."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
            
        self.is_running = True
        logger.info("Starting post scheduler...")
        
        while self.is_running:
            try:
                await self.check_and_post_scheduled_posts()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(self.check_interval)
    
    async def stop(self):
        """Stop the scheduler service."""
        self.is_running = False
        logger.info("Stopping post scheduler...")
    
    async def check_and_post_scheduled_posts(self):
        """Check for posts that need to be posted and post them."""
        try:
            db = get_database()
            
            # Get posts that are scheduled and due for posting
            now = datetime.now()
            scheduled_posts = await db[POSTS_COLLECTION].find({
                "status": "scheduled",
                "scheduled_date": {
                    "$lte": now.isoformat()
                }
            }).to_list(length=None)
            
            if not scheduled_posts:
                return
            
            logger.info(f"Found {len(scheduled_posts)} posts to post")
            
            for post in scheduled_posts:
                try:
                    await self.post_single_post(post)
                except Exception as e:
                    logger.error(f"Error posting post {post['_id']}: {e}")
                    # Mark post as failed
                    await db[POSTS_COLLECTION].update_one(
                        {"_id": post["_id"]},
                        {
                            "$set": {
                                "status": "failed",
                                "error_message": str(e),
                                "updated_at": now.isoformat()
                            }
                        }
                    )
                    
        except Exception as e:
            logger.error(f"Error checking scheduled posts: {e}")
    
    async def post_single_post(self, post: Dict[str, Any]):
        """Post a single post to all connected platforms."""
        try:
            db = get_database()
            now = datetime.now()
            
            # Get user's platform connections
            user = await db[USERS_COLLECTION].find_one({"_id": post["user_id"]})
            if not user:
                logger.error(f"User not found for post {post['_id']}")
                return
            
            # Check which platforms are connected
            connected_platforms = []
            
            # Check LinkedIn connection
            if hasattr(linkedin_token_manager, 'get_user_token'):
                linkedin_token = await linkedin_token_manager.get_user_token(str(user["_id"]))
                if linkedin_token:
                    connected_platforms.append("linkedin")
            
            # TODO: Add checks for other platforms (Instagram, Facebook, Twitter)
            # For now, we'll just simulate posting to connected platforms
            
            if connected_platforms:
                # Post to connected platforms
                for platform in connected_platforms:
                    if platform == "linkedin" and "linkedin" in post.get("platforms", []):
                        await self.post_to_linkedin(post, user)
                    # Add other platform posting logic here
                
                # Mark post as posted
                await db[POSTS_COLLECTION].update_one(
                    {"_id": post["_id"]},
                    {
                        "$set": {
                            "status": "posted",
                            "posted_at": now.isoformat(),
                            "posted_to": connected_platforms,
                            "updated_at": now.isoformat()
                        }
                    }
                )
                
                logger.info(f"Successfully posted post {post['_id']} to {connected_platforms}")
                
                # Send success notification
                try:
                    from utils.notifications import notify_posting_success
                    await notify_posting_success(str(user["_id"]), 1, connected_platforms)
                except Exception as e:
                    logger.error(f"Error sending posting success notification: {e}")
            else:
                # No platforms connected, mark as posted anyway
                await db[POSTS_COLLECTION].update_one(
                    {"_id": post["_id"]},
                    {
                        "$set": {
                            "status": "posted",
                            "posted_at": now.isoformat(),
                            "posted_to": [],
                            "updated_at": now.isoformat()
                        }
                    }
                )
                logger.info(f"Post {post['_id']} marked as posted (no platforms connected)")
                
        except Exception as e:
            logger.error(f"Error posting single post {post['_id']}: {e}")
            raise
    
    async def post_to_linkedin(self, post: Dict[str, Any], user: Dict[str, Any]):
        """Post content to LinkedIn."""
        try:
            # Prepare the content for LinkedIn
            content = post.get("caption", "")
            hashtags = post.get("hashtags", [])
            
            if hashtags:
                content += "\n\n" + " ".join(hashtags[:5])  # Limit to 5 hashtags
            
            # Post to LinkedIn
            result = await linkedin_service.post_content(
                user_id=str(user["_id"]),
                content=content,
                image_url=post.get("image_url")
            )
            
            logger.info(f"Posted to LinkedIn: {result}")
            
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            raise
    
    async def schedule_posts_for_user(self, user_id: str, schedule_time: str = "09:00"):
        """Schedule all approved posts for a user at the specified time."""
        try:
            db = get_database()
            
            # Get all approved posts for the user
            approved_posts = await db[POSTS_COLLECTION].find({
                "user_id": user_id,
                "status": "approved"
            }).to_list(length=None)
            
            if not approved_posts:
                logger.info(f"No approved posts found for user {user_id}")
                return
            
            # Parse schedule time
            hour, minute = map(int, schedule_time.split(":"))
            
            for post in approved_posts:
                # Parse the scheduled date and set the time
                scheduled_date = datetime.fromisoformat(post["scheduled_date"])
                scheduled_date = scheduled_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # Update the post with the new scheduled date
                await db[POSTS_COLLECTION].update_one(
                    {"_id": post["_id"]},
                    {
                        "$set": {
                            "scheduled_date": scheduled_date.isoformat(),
                            "status": "scheduled",
                            "updated_at": datetime.now().isoformat()
                        }
                    }
                )
            
            logger.info(f"Scheduled {len(approved_posts)} posts for user {user_id} at {schedule_time}")
            
        except Exception as e:
            logger.error(f"Error scheduling posts for user {user_id}: {e}")
            raise

# Global scheduler instance
scheduler = PostScheduler()

async def start_scheduler():
    """Start the global scheduler."""
    await scheduler.start()

async def stop_scheduler():
    """Stop the global scheduler."""
    await scheduler.stop()

async def schedule_user_posts(user_id: str, schedule_time: str = "09:00"):
    """Schedule posts for a specific user."""
    await scheduler.schedule_posts_for_user(user_id, schedule_time) 