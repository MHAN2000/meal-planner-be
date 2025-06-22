# app/schemas/recipe.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RecipeBase(BaseModel):
    name: Optional[str] = None
    instructions: Optional[str] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    photo: Optional[str] = None

class RecipeCreate(RecipeBase):
    user_id: int
    name: str
    instructions: str
    prep_time: int
    cook_time: int
    pass

class RecipeUpdate(RecipeBase):
    pass

class RecipeInDBBase(RecipeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RecipeResponse(RecipeInDBBase):
    pass
