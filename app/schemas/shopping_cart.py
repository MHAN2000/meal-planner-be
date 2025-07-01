from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ShoppingCartBase(BaseModel):
    ingredient_id: Optional[int] = None
    user_id: Optional[int] = None
    date: Optional[datetime] = None
    qty: Optional[int] = None

class ShoppingCartCreate(ShoppingCartBase):
    pass

class ShoppingCartUpdate(BaseModel):
    ingredient_id: Optional[int] = None
    date: Optional[datetime] = None
    qty: Optional[int] = None

class ShoppingCartInDBBase(SHoppingCartBase):
    id: Optional[int] = None
    ingredient_id: Optional[int] = None
    user_id: Optional[int] = None
    date: Optional[datetime] = None
    qty: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ShoppingCartResponse(ShoppingCartInDBBase):
    pass