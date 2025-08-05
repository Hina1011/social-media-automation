import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
import logging
from jinja2 import Template

logger = logging.getLogger(__name__)


async def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Send an email using SMTP."""
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.email_username
        message["To"] = to_email

        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        await aiosmtplib.send(
            message,
            hostname=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.email_username,
            password=settings.email_password,
            use_tls=True
        )
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False


async def send_otp_email(email: str, otp: str) -> bool:
    """Send OTP email."""
    subject = "Your Verification Code - Social Media Automation"
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Verification Code</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
            .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
            .otp-code { background: #fff; padding: 20px; text-align: center; 
                       font-size: 32px; font-weight: bold; color: #667eea; 
                       border-radius: 8px; margin: 20px 0; letter-spacing: 5px; }
            .footer { text-align: center; margin-top: 20px; color: #666; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 Verification Code</h1>
                <p>Social Media Automation Platform</p>
            </div>
            <div class="content">
                <h2>Hello!</h2>
                <p>You've requested a verification code for your Social Media Automation account.</p>
                
                <div class="otp-code">{{ otp }}</div>
                
                <p><strong>This code will expire in 10 minutes.</strong></p>
                
                <p>If you didn't request this code, please ignore this email.</p>
                
                <p>Best regards,<br>The Social Media Automation Team</p>
            </div>
            <div class="footer">
                <p>This is an automated message, please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    template = Template(html_template)
    html_content = template.render(otp=otp)
    
    return await send_email(email, subject, html_content)


async def send_welcome_email(email: str, full_name: str) -> bool:
    """Send welcome email after successful registration."""
    subject = "Welcome to Social Media Automation!"
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Welcome</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
            .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
            .cta-button { display: inline-block; background: #667eea; color: white; 
                         padding: 15px 30px; text-decoration: none; border-radius: 5px; 
                         margin: 20px 0; }
            .footer { text-align: center; margin-top: 20px; color: #666; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome!</h1>
                <p>Social Media Automation Platform</p>
            </div>
            <div class="content">
                <h2>Hello {{ full_name }}!</h2>
                <p>Welcome to the Social Media Automation Platform! 🚀</p>
                
                <p>You're now ready to:</p>
                <ul>
                    <li>Generate AI-powered content for your social media</li>
                    <li>Schedule posts across multiple platforms</li>
                    <li>Track your growth and engagement</li>
                    <li>Automate your social media presence</li>
                </ul>
                
                <p><strong>Next steps:</strong></p>
                <ol>
                    <li>Complete your profile setup</li>
                    <li>Connect your social media accounts</li>
                    <li>Generate your first batch of content</li>
                    <li>Start automating!</li>
                </ol>
                
                <a href="{{ base_url }}/dashboard" class="cta-button">Go to Dashboard</a>
                
                <p>If you have any questions, feel free to reach out to our support team.</p>
                
                <p>Best regards,<br>The Social Media Automation Team</p>
            </div>
            <div class="footer">
                <p>Thank you for choosing us!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    template = Template(html_template)
    html_content = template.render(full_name=full_name, base_url=settings.base_url)
    
    return await send_email(email, subject, html_content) 