from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from bson import ObjectId
from .user import PyObjectId


class PostBase(BaseModel):
    caption: str = Field(..., min_length=10, max_length=2200)
    hashtags: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    scheduled_date: datetime
    platforms: List[Literal["instagram", "linkedin", "facebook", "twitter"]] = Field(..., min_items=1)
    status: Literal["draft", "approved", "posted", "failed"] = "draft"
    custom_prompt: Optional[str] = None


class PostCreate(PostBase):
    user_id: PyObjectId = Field(default_factory=PyObjectId)


class PostUpdate(BaseModel):
    caption: Optional[str] = Field(None, min_length=10, max_length=2200)
    hashtags: Optional[List[str]] = None
    image_url: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    platforms: Optional[List[Literal["instagram", "linkedin", "facebook", "twitter"]]] = None
    status: Optional[Literal["draft", "approved", "posted", "failed"]] = None


class PostInDB(PostBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    posted_at: Optional[datetime] = None
    engagement_data: Optional[dict] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Post(PostBase):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    posted_at: Optional[datetime] = None
    engagement_data: Optional[dict] = None
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class PostBatch(BaseModel):
    posts: List[PostCreate]
    batch_start_date: datetime
    batch_end_date: datetime
    user_id: PyObjectId = Field(default_factory=PyObjectId)


class PostGenerationRequest(BaseModel):
    custom_prompt: str = Field(..., min_length=10, max_length=500)
    start_date: datetime
    platforms: List[Literal["instagram", "linkedin", "facebook", "twitter"]] = Field(..., min_items=1)
    posting_days: Optional[List[int]] = None  # Days of week (0=Monday, 6=Sunday)


class PostApprovalRequest(BaseModel):
    post_ids: List[str] = Field(..., min_items=1)
    approve_all: bool = False 