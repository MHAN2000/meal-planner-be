from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    
class UserCreate(UserBase):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length = 255)
    password: str = Field(..., min_length=8)
    
class UserUpdate(UserBase):
    password: Optional[str] = None
    
class UserInDBBase(UserBase):
    id: Optional[int] = None
    password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
class UserResponse(UserInDBBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class TokenData(BaseModel):
    email: Optional[str] = None