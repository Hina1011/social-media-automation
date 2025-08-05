from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from .user import PyObjectId


class AnalyticsBase(BaseModel):
    platform: str
    date: datetime
    followers_count: int = 0
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    impressions_count: int = 0
    reach_count: int = 0
    engagement_rate: float = 0.0


class AnalyticsCreate(AnalyticsBase):
    user_id: PyObjectId = Field(default_factory=PyObjectId)


class AnalyticsUpdate(BaseModel):
    followers_count: Optional[int] = None
    likes_count: Optional[int] = None
    comments_count: Optional[int] = None
    shares_count: Optional[int] = None
    impressions_count: Optional[int] = None
    reach_count: Optional[int] = None
    engagement_rate: Optional[float] = None


class AnalyticsInDB(AnalyticsBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Analytics(AnalyticsBase):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class AnalyticsSummary(BaseModel):
    total_followers: int
    total_engagement: int
    average_engagement_rate: float
    platform_breakdown: Dict[str, Dict[str, Any]]
    growth_trend: List[Dict[str, Any]]
    top_posts: List[Dict[str, Any]]


class AnalyticsRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    platforms: Optional[List[str]] = None 