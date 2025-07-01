# app/routers/shopping_cart.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.services.shopping_carts import ShoppingCartService
from app.schemas.shopping_cart import ShoppingCartCreate, ShoppingCartUpdate, ShoppingCartResponse

from app.security import get_current_active_user
from app.models.user import User
from app.models.category import Category

router = APIRouter(
    prefix="/shopping_cart",
    tags=["shopping_cart"]
)

shopping_cart_service = ShoppingCartService()

@router.get('/', response_model=List[ShoppingCartResponse])
async def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    shopping_carts = shopping_cart_service.get_all_shopping_carts()
    return shopping_carts

@router.post('/', response_model=ShoppingCartResponse, status_code=status.HTTP_201_CREATED)
async def store(req: ShoppingCartCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user())):
    shopping_cart = shopping_cart_service.create_shopping_cart(db, req)
    return shopping_cart

@router.put('/{id}', response_model=ShoppingCartResponse, status_code=status.HTTP_200_OK)
async def update(id: int, req: ShoppingCartUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user())):
    existing_shopping_cart = db.scalars(select(ShoppingCart).where(ShoppingCart.id == id)).first()
    if not existing_shopping_cart:
        raise HTTPException(status_code=404, detail=f"Shopping card with id {id} not found")

    updated_shopping_cart = shopping_cart_service.update(db, existing_shopping_cart, req)

    return updated_shopping_cart

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted = shopping_cart_service.destroy(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Shopping card with id {id} not found")

    return