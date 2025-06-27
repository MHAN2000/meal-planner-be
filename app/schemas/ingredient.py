from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class IngredientBase(BaseModel):
    ingredient: Optional[str] = None

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(IngredientBase):
    pass

class IngredientInDBBase(IngredientBase):
    id: Optional[int] = None
    ingredient: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class IngredientResponse(IngredientInDBBase):
    pass
