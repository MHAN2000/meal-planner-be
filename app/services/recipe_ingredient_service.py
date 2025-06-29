# app/services/recipe_ingredient_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List
import json

from app.models.recipe_ingredient import RecipeIngredient
from app.schemas.recipe_ingredient import RecipeIngredientCreate, RecipeIngredientUpdate, RecipeIngredientResponse
from app.redis_client import redis_client
from app.config import settings

class RecipeIngredientService:
    def get_all_recipe_ingredients_from_db(self, db):
        return db.scalars(select(RecipeIngredient).where(RecipeIngredient.deleted_at.is_(None))).all()

    def get_all_recipe_ingredients(self, db: Session) -> List[RecipeIngredient]:
        cached_data = redis_client.get("recipe_ingredients")
        if cached_data:
            return [RecipeIngredient(**item) for item in json.loads(cached_data)]

        recipe_ingredients = self.get_all_recipe_ingredients_from_db(db)
        recipe_ingredients_response_data = [RecipeIngredientResponse.model_validate(ingredient).model_dump(mode='json') for ingredient in recipe_ingredients]
        print(recipe_ingredients_response_data)
        redis_client.setex("recipe_ingredients", settings.REDIS_CACHE_EXPIRE_SECONDS, json.dumps(recipe_ingredients_response_data))

        return settings

    def update (self, db: Session, db_recipe_ingredient: RecipeIngredient, req: RecipeIngredientUpdate) -> RecipeIngredient:
        update_data = req.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_recipe_ingredient, field, value)

        db.add(db_recipe_ingredient)
        db.commit()
        db.refresh(db_recipe_ingredient)

        redis_client.delete("recipe_ingredients")
        return db_recipe_ingredient

    def destroy(self, db: Session, id: int) -> bool:
        recipe_ingredient = db.scalars(select(RecipeIngredient).get(id))
        if not recipe_ingredient:
            return False

        recipe_ingredient.deleted_at = func.now()

        db.add(recipe_ingredient)
        db.commit()
        db.refresh(recipe_ingredient)

        return True

    def create_recipe_ingredient(self, db: Session, req: RecipeIngredientCreate) -> RecipeIngredient:
        db_recipe_ingredient = RecipeIngredient(**req.model_dump())
        db.add(db_recipe_ingredient)
        db.commit()
        db.refresh(db_recipe_ingredient)

        redis_client.delete("recipe_ingredients")
        return db_recipe_ingredient


