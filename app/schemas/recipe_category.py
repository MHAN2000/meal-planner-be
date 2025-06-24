from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RecipeCategoryBase(BaseModel):
    recipe_id: int
    category_id: int

class RecipeCategoryCreate(RecipeCategoryBase):
    pass

class RecipeCategoryUpdate(RecipeCategoryBase):
    pass

class RecipeCategoryInDBBase(RecipeCategoryBase):
    id: int
    recipe_id: int
    category_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RecipeCategoryResponse(RecipeCategoryInDBBase):
    pass
