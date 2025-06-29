from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List
import json

from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate, IngredientUpdate, IngredientResponse
from app.redis_client import redis_client
from app.config import settings

class IngredientService:
    def get_all_ingredients_from_db(self, db: Session) -> List[Ingredient]:
        return db.scalars(select(Ingredient).where(Ingredient.deleted_at.is_(None))).all()

    def get_all_ingredients(self, db: Session) -> List[Ingredient]:
        cached_data = redis_client.get("ingredients")
        if cached_data:
            return [Ingredient(**item) for item in json.loads(cached_data)]

        ingredients = self.get_all_ingredients_from_db(db)
        ingredients_response_date = [IngredientResponse.model_validate(c).model_dump(mode='json') for c in ingredients]
        redis_client.setex("ingredients", settings.REDIS_CACHE_EXPIRE_SECONDS, json.dumps(ingredients_response_date))

        return ingredients

    def destroy(self, db: Session, id: int) -> bool:
        ingredient = db.query(Ingredient).get(id)
        if not ingredient:
            return False

        ingredient.deleted_at = func.now()
        db.add(ingredient)
        db.commit()
        db.refresh(ingredient)

        redis_client.delete("ingredients")

        return True

    def create_ingredient(self, db: Session, req: IngredientCreate) -> Ingredient:
        db_ingredient = Ingredient(**req.model_dump())
        db.add(db_ingredient)
        db.commit()
        db.refresh(db_ingredient)

        redis_client.delete("ingredients")
        return db_ingredient

    def update(self, db: Session, db_ingredient: Ingredient, req: IngredientUpdate) -> Ingredient:
        update_data = req.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ingredient, field, value)

        db.add(db_ingredient)
        db.commit()
        db.refresh(db_ingredient)

        redis_client.delete("ingredients")

        return db_ingredient
