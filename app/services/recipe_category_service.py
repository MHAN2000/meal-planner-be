from app.config import settings
from app.models.recipe_category import RecipeCategory
from app.redis_client import redis_client
from sqlalchemy.orm import Session
from typing import Optional, List
from app.schemas.recipe_category import RecipeCategoryResponse, RecipeCategoryCreate, RecipeCategoryUpdate
from sqlalchemy import select, func
import json



class RecipeCategoryService:
    def get_all_recipe_categories_from_db(self, db: Session) ->List[RecipeCategory]:
        return db.scalars(select(RecipeCategory).where(RecipeCategory.deleted_at.isnot(None)))

    def get_all_recipe_categories(self, db: Session) -> List[RecipeCategory]:
        cached_data = redis_client.get("recipe_categories")
        if cached_data:
            return [RecipeCategory(**item) for item in json.loads(cached_data)]

        recipe_categories = self.get_all_recipe_categories_from_db(db)
        recipe_categories_response_data = [RecipeCategory.model_validate(c).model_dump(mode='json') for c in recipe_categories]
        redis_client.setex("recipe_categories", settings.REDIS_CACHE_EXPIRE_SECONDS, json.dumps(recipe_categories_response_data))

        return recipe_categories

    def update(self, db: Session, db_recipe_category: RecipeCategory, req: RecipeCategoryUpdate) -> RecipeCategory:
        update_data = req.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_recipe_category, field, value)

        db.add(db_recipe_category)
        db.commit()
        db.refresh(db_recipe_category)

        redis_client.delete("recipe_categories")

        return db_recipe_category


    def create_recipe_category(self, db: Session, req: RecipeCategoryCreate) -> RecipeCategory:
        db_recipe_category = RecipeCategory(**req.model_dump())
        db.add(db_recipe_category)
        db.commit()
        db.refresh(db_recipe_category)

        redis_client.delete("recipe_categories")
        return db_recipe_category

    def destroy(self, db: Session, id: int) -> bool:
        recipe_category = db.scalars(select(RecipeCategory).where(RecipeCategory.id == id)).first()
        if not recipe_category:
            return False

        recipe_category.deleted_at = func.now()
        db.add(recipe_category)
        db.commit()
        db.refresh(recipe_category)

        redis_client.delete("recipe_categories")

        return True