# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Shared properties
class CategoryBase(BaseModel):
    category: Optional[str] = None
    is_active: Optional[bool] = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    category: Optional[str] = None
    is_active: Optional[bool] = None

class CategoryInDBBase(CategoryBase):
    id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
class CategoryResponse(CategoryInDBBase):
    pass