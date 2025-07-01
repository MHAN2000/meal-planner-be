# app/services/shopping_cart_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List
import json

from app.models.shopping_cart import ShoppingCart
from app.schemas.shopping_cart import ShoppingCartCreate, ShoppingCartUpdate, ShoppingCartResponse
from app.redis_client import redis_client
from app.config import settings

class ShoppingCartService:
    def get_all_shopping_carts_from_db(self, db: Session) -> List[ShoppingCart]:
        return db.scalars(select(ShoppingCart).where(ShoppingCart.deleted_at.is_(None))).all()

    def get_all_shopping_carts(self, db: Session)-> List[ShoppingCart]:
        cached_data = redis_client.get("shopping_carts")
        if cached_data:
            return [ShoppingCart(**item) for item in json.loads(cached_data)]

        shopping_carts = self.get_all_shopping_carts_from_db(db)
        shopping_carts_response_data = [ShoppingCartResponse.model_validate(c).model_dump(mode='json') for c in shopping_carts]
        redis_client.setex("shopping_carts", settings.REDIS_CACHE_EXPIRE_SECONDS, json.dumps(shopping_carts_response_data))

        return shopping_carts

    def update(self, db: Session, db_shopping_cart: ShoppingCart, req: ShoppingCartUpdate) -> None:
        update_data = req.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_shopping_cart, field, value)

        db.add(db_shopping_cart)
        db.commit()
        db.refresh(db_shopping_cart)

        redis_client.delete("shopping_carts")

        return db_shopping_cart

    def destroy(self, db: Session, id: int) -> None:
        shopping_cart = db.scalars(select(ShoppingCart).where(ShoppingCart.id == id)).first()
        if not shopping_cart:
            return False

        shopping_cart.deleted_at = func.now()
        db.add(shopping_cart)
        db.commit()
        db.refresh(shopping_cart)

        redis_client.delete("shopping_carts")

        return True

    def create_shopping_cart(self, db: Session, req: ShoppingCartCreate) -> ShoppingCart:
        db_shopping_cart = ShoppingCart(**req.model_dump())
        db.add(db_shopping_cart)
        db.commit()
        db.refresh(db_shopping_cart)

        redis_client.delete("shopping_carts")
        return db_shopping_cart
    