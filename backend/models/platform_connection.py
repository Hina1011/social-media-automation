from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId
from .user import PyObjectId


class PlatformConnectionBase(BaseModel):
    platform: Literal["instagram", "linkedin", "facebook", "twitter"]
    is_connected: bool = False
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    platform_user_id: Optional[str] = None
    platform_username: Optional[str] = None
    expires_at: Optional[datetime] = None


class PlatformConnectionCreate(PlatformConnectionBase):
    user_id: PyObjectId = Field(default_factory=PyObjectId)


class PlatformConnectionUpdate(BaseModel):
    is_connected: Optional[bool] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    platform_user_id: Optional[str] = None
    platform_username: Optional[str] = None
    expires_at: Optional[datetime] = None


class PlatformConnectionInDB(PlatformConnectionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class PlatformConnection(PlatformConnectionBase):
    id: str = Field(alias="_id")
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class PlatformAuthRequest(BaseModel):
    platform: Literal["instagram", "linkedin", "facebook", "twitter"]
    auth_code: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    state: Optional[str] = None


class PlatformAuthResponse(BaseModel):
    platform: str
    auth_url: Optional[str] = None
    success: bool
    message: str 