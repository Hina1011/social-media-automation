from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from config import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None
    sync_client: MongoClient = None
    is_connected: bool = False


db = Database()


async def connect_to_mongo():
    """Create database connection."""
    try:
        logger.info(f"Attempting to connect to MongoDB with URL: {settings.MONGODB_URL}")
        
        # For MongoDB Atlas, use the connection string as is
        connection_string = settings.MONGODB_URL
        
        # Create clients with proper configuration
        db.client = AsyncIOMotorClient(connection_string, serverSelectionTimeoutMS=10000)
        db.sync_client = MongoClient(connection_string, serverSelectionTimeoutMS=10000)
        
        # Test the connection
        await db.client.admin.command('ping')
        db.is_connected = True
        logger.info("Successfully connected to MongoDB")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        # Don't raise the exception, just log it
        logger.warning("Database connection failed, but application will continue")
        # Try to create clients anyway for lazy connection
        try:
            db.client = AsyncIOMotorClient(connection_string)
            db.sync_client = MongoClient(connection_string)
            db.is_connected = False  # Mark as not connected but clients exist
        except Exception as client_error:
            logger.error(f"Failed to create MongoDB clients: {client_error}")
            db.client = None
            db.sync_client = None
            db.is_connected = False


async def close_mongo_connection():
    """Close database connection."""
    try:
        if db.client:
            db.client.close()
        if db.sync_client:
            db.sync_client.close()
        db.is_connected = False
        logger.info("Successfully closed MongoDB connection")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")


def get_database():
    """Get database instance."""
    if db.client is None:
        logger.error("Database connection not available")
        raise Exception("Database connection not available. Please check your MongoDB connection.")
    return db.client[settings.DATABASE_NAME]


def get_sync_database():
    """Get synchronous database instance."""
    if db.sync_client is None:
        logger.error("Database connection not available")
        raise Exception("Database connection not available. Please check your MongoDB connection.")
    return db.sync_client[settings.DATABASE_NAME]


def is_database_connected():
    """Check if database is connected."""
    return db.is_connected


# Collection names
USERS_COLLECTION = "users"
POSTS_COLLECTION = "posts"
PLATFORM_CONNECTIONS_COLLECTION = "platform_connections"
ANALYTICS_COLLECTION = "analytics"
OTP_COLLECTION = "otp_codes" 