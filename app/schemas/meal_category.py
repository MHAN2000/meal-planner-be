# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Shared properties
class MealCategoryBase(BaseModel):
    category: Optional[str] = None
    is_active: Optional[bool] = True

class MealCategoryCreate(MealCategoryBase):
    pass

class MealCategoryUpdate(MealCategoryBase):
    category: Optional[str] = None

class MealCategoryInDBBase(MealCategoryBase):
    id: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
class MealCategoryResponse(MealCategoryInDBBase):
    pass