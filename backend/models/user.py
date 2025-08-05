from pydantic import BaseModel, EmailStr, Field, GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from typing import List, Optional, Literal
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.str_schema()
    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler) -> JsonSchemaValue:
        return {"type": "string"}


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    mobile_number: str = Field(..., pattern=r'^\+?1?\d{9,15}$')
    profession: str = Field(..., min_length=2, max_length=200)
    interests: List[str] = Field(..., min_items=5, max_items=20)
    custom_prompt: str = Field(..., min_length=10, max_length=500)
    role: Literal["individual", "company"] = "individual"
    
    # Company-specific fields (optional)
    company_name: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    mobile_number: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    profession: Optional[str] = Field(None, min_length=2, max_length=200)
    interests: Optional[List[str]] = Field(None, min_items=5, max_items=20)
    custom_prompt: Optional[str] = Field(None, min_length=10, max_length=500)
    company_name: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None


class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str
    is_verified: bool = False
    is_profile_complete: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class User(UserBase):
    id: str = Field(alias="_id")
    is_verified: bool
    is_profile_complete: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None 