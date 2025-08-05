from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import settings
from database import connect_to_mongo, close_mongo_connection, db
from utils import verify_token

# Import routers
from routers import auth, users, posts, platforms, analytics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Social Media Automation Platform...")
    try:
        await connect_to_mongo()
        logger.info("MongoDB connection successful!")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        logger.warning("Application will start without database connection. Some features may not work.")
    
    # Create static directories
    os.makedirs("static/images/generated", exist_ok=True)
    os.makedirs("static/images/placeholder", exist_ok=True)
    
    logger.info("Application startup complete!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Social Media Automation Platform...")
    try:
        await close_mongo_connection()
        logger.info("MongoDB connection closed successfully!")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")
    logger.info("Application shutdown complete!")


# Create FastAPI app
app = FastAPI(
    title="Social Media Content Automation Platform",
    description="A comprehensive platform for automating social media content creation and scheduling",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    email = verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return email


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
logger.info("Registering platform routes...")
app.include_router(
    platforms.router,
    prefix="/api",
    tags=["Platform Connections"]
)
logger.info("Platform routes registered")
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Social Media Content Automation Platform API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    from datetime import datetime
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if hasattr(db, 'client') and db.client else "disconnected"
    }


@app.get("/api/protected")
async def protected_route(current_user: str = Depends(get_current_user)):
    """Protected route example."""
    return {"message": f"Hello {current_user}, this is a protected route!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 