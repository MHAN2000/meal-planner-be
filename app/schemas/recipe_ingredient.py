from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class RecipeIngredientBase(BaseModel):
    ingredient_id: Optional[int] = None
    recipe_id: Optional[int] = None
    qty: Optional[int] = None

class RecipeIngredientCreate(RecipeIngredientBase):
    pass

class RecipeIngredientUpdate(RecipeIngredientBase):
    pass

class RecipeIngredientInDBBase(RecipeIngredientBase):
    id: Optional[int] = None
    ingredient_id: Optional[int] = None
    recipe_id: Optional[int] = None
    qty: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RecipeIngredientResponse(RecipeIngredientInDBBase):
    pass
