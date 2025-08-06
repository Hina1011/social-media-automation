import logging
from typing import List, Dict, Any
from database import get_database, USERS_COLLECTION, POSTS_COLLECTION
from utils.email import send_email

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.db = get_database()
    
    async def send_batch_ready_notification(self, user_id: str, batch_id: str, post_count: int):
        """Send notification when a new batch is ready for approval."""
        try:
            # Get user information
            user = await self.db[USERS_COLLECTION].find_one({"_id": user_id})
            if not user:
                logger.error(f"User not found for notification: {user_id}")
                return
            
            # Prepare email content
            subject = "New Posts Ready for Approval"
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #2563eb;">New Posts Ready for Approval</h2>
                <p>Hello {user.get('full_name', 'there')},</p>
                <p>Your AI has generated <strong>{post_count} new posts</strong> and they're ready for your review!</p>
                
                <div style="background-color: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 16px; margin: 20px 0;">
                    <h3 style="color: #92400e; margin-top: 0;">What happens next?</h3>
                    <ul style="color: #92400e;">
                        <li>Review your generated posts</li>
                        <li>Approve the ones you like</li>
                        <li>Posts will be automatically scheduled and posted</li>
                        <li>New batch will be generated after current one is approved</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:3000/posts" 
                       style="background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                        Review Posts Now
                    </a>
                </div>
                
                <p style="color: #6b7280; font-size: 14px;">
                    This is an automated notification from your Social Media Automation Platform.
                </p>
            </div>
            """
            
            # Send email
            await send_email(
                to_email=user["email"],
                subject=subject,
                html_content=html_content
            )
            
            logger.info(f"Sent batch ready notification to {user['email']}")
            
        except Exception as e:
            logger.error(f"Error sending batch ready notification: {e}")
    
    async def send_approval_reminder(self, user_id: str, pending_count: int):
        """Send reminder for pending approvals."""
        try:
            # Get user information
            user = await self.db[USERS_COLLECTION].find_one({"_id": user_id})
            if not user:
                logger.error(f"User not found for reminder: {user_id}")
                return
            
            # Prepare email content
            subject = "Reminder: Posts Pending Approval"
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #dc2626;">Posts Pending Approval</h2>
                <p>Hello {user.get('full_name', 'there')},</p>
                <p>You have <strong>{pending_count} posts</strong> waiting for your approval.</p>
                
                <div style="background-color: #fef2f2; border: 1px solid #ef4444; border-radius: 8px; padding: 16px; margin: 20px 0;">
                    <h3 style="color: #991b1b; margin-top: 0;">Why approve now?</h3>
                    <ul style="color: #991b1b;">
                        <li>Keep your content calendar active</li>
                        <li>Maintain consistent posting schedule</li>
                        <li>Generate new content automatically</li>
                        <li>Maximize your social media presence</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:3000/posts" 
                       style="background-color: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                        Review Posts Now
                    </a>
                </div>
                
                <p style="color: #6b7280; font-size: 14px;">
                    This is an automated reminder from your Social Media Automation Platform.
                </p>
            </div>
            """
            
            # Send email
            await send_email(
                to_email=user["email"],
                subject=subject,
                html_content=html_content
            )
            
            logger.info(f"Sent approval reminder to {user['email']}")
            
        except Exception as e:
            logger.error(f"Error sending approval reminder: {e}")
    
    async def send_posting_success_notification(self, user_id: str, post_count: int, platforms: List[str]):
        """Send notification when posts are successfully posted."""
        try:
            # Get user information
            user = await self.db[USERS_COLLECTION].find_one({"_id": user_id})
            if not user:
                logger.error(f"User not found for success notification: {user_id}")
                return
            
            # Prepare email content
            subject = "Posts Successfully Published"
            platforms_text = ", ".join(platforms) if platforms else "your connected platforms"
            
            html_content = f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #059669;">Posts Successfully Published</h2>
                <p>Hello {user.get('full_name', 'there')},</p>
                <p>Great news! <strong>{post_count} posts</strong> have been successfully published to {platforms_text}.</p>
                
                <div style="background-color: #ecfdf5; border: 1px solid #10b981; border-radius: 8px; padding: 16px; margin: 20px 0;">
                    <h3 style="color: #065f46; margin-top: 0;">What's happening?</h3>
                    <ul style="color: #065f46;">
                        <li>Your content is reaching your audience</li>
                        <li>Engagement metrics are being tracked</li>
                        <li>New batch will be generated soon</li>
                        <li>Your social media presence is growing</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:3000/analytics" 
                       style="background-color: #059669; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                        View Analytics
                    </a>
                </div>
                
                <p style="color: #6b7280; font-size: 14px;">
                    This is an automated notification from your Social Media Automation Platform.
                </p>
            </div>
            """
            
            # Send email
            await send_email(
                to_email=user["email"],
                subject=subject,
                html_content=html_content
            )
            
            logger.info(f"Sent posting success notification to {user['email']}")
            
        except Exception as e:
            logger.error(f"Error sending posting success notification: {e}")

# Global notification service instance
notification_service = NotificationService()

async def notify_batch_ready(user_id: str, batch_id: str, post_count: int):
    """Notify user that a new batch is ready for approval."""
    await notification_service.send_batch_ready_notification(user_id, batch_id, post_count)

async def notify_approval_reminder(user_id: str, pending_count: int):
    """Send reminder for pending approvals."""
    await notification_service.send_approval_reminder(user_id, pending_count)

async def notify_posting_success(user_id: str, post_count: int, platforms: List[str]):
    """Notify user when posts are successfully posted."""
    await notification_service.send_posting_success_notification(user_id, post_count, platforms) 