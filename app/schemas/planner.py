from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PlannerBase(BaseModel):
    recipe_id: Optional[int] = None
    user_id = Optional[int] = None
    date: Optional[datetime] = None

class PlannerCreate(PlannerBase):
    pass

class PlannerUpdate(PlannerBase):
    pass

class PlannerInDBBase(PlannerBase):
    id: Optional[int] = None
    recipe_id: Optional[int] = None
    user_id: Optional[int] = None
    date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PlannerResponse(PlannerInDBBase):
    pass
