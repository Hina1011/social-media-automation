from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database Configuration
    mongodb_url: str = "mongodb://localhost:27017"  # Default fallback
    database_name: str = "social_media_automation"
    
    # JWT Configuration
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Email Configuration
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    email_username: str = ""
    email_password: str = ""
    
    # AI Configuration
    gemini_api_key: str = ""
    
    # Image Generation APIs (Free Options Only)
    openai_api_key: str = ""
    unsplash_access_key: str = ""
    
    # LinkedIn OAuth Configuration
    linkedin_client_id: str = "78ezba5uscu27i"
    linkedin_client_secret: str = "WPL_AP1.TRmef0zZ05LpG9DS.Np0p8w=="
    linkedin_redirect_uri: str = "http://localhost:3000/linkedin-callback"
    linkedin_scope: str = "r_liteprofile r_emailaddress w_member_social"
    
    # Manual LinkedIn Access Token (temporary - use .env file for production)
    linkedin_access_token: str = ""  # Add your access token here
    linkedin_refresh_token: str = ""  # Add your refresh token here
    
    # Other Social Media API Keys
    facebook_app_id: str = ""
    facebook_app_secret: str = ""
    twitter_api_key: str = ""
    twitter_api_secret: str = ""
    twitter_access_token: str = ""
    twitter_access_token_secret: str = ""
    instagram_username: str = ""
    instagram_password: str = ""
    
    # Application Configuration
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    base_url: str = "http://localhost:8000"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


settings = Settings() 