from app.config import settings
from app.models.recipe import Recipe
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os
from pathlib import Path

import json

from app.redis_client import redis_client
from app.schemas.recipe import RecipeResponse, RecipeCreate


class RecipeService:
    def get_recipes_from_db(self, db: Session) -> List[Recipe]:
        return db.scalars(select(Recipe).where(Recipe.deleted_at.is_(None))).all()

    def get_recipes(self, db: Session) -> List[Recipe]:
        cached_date = redis_client.get("recipes")
        if cached_date:
            print("DEBUG: Cache hit for recipes")
            return [Category(**item) for item in json.loads(cached_date)]

        print("DEBUG: Cache miss for recipes, fetching from db")

        recipes = self.get_recipes_from_db(db)
        recipes_response_data = [RecipeResponse.model_validate(c).model_dump(mode="json") for c in recipes]
        redis_client.setex("recipes", settings.REDIS_CACHE_EXPIRE_SECONDS, json.dumps(recipes_response_data))

        return recipes

    def create_recipe(self, db: Session, recipe_in: RecipeCreate, photo_file_bytes: Optional[bytes] = None,
                      photo_filename: Optional[str] = None) -> Recipe:

        photo_path_for_db = None  # Relative path to store in db

        if photo_file_bytes and photo_filename:
            # 1. Create the folder if it does not exist
            upload_dir = Path(settings.UPLOADS_DIR)
            upload_dir.mkdir(parents=True, exist_ok=True)

            # 2. Generate an unique name for the file
            file_extension = Path(photo_filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_extension}"

            # 3. Build the full path in the server
            file_location = upload_dir / unique_filename

            # 4. Save the file
            with open(file_location, "wb") as file_obj:
                file_obj.write(photo_file_bytes)

            # 5. Save the relative path
            photo_path_for_db = f"/{settings.UPLOADS_DIR}/{unique_filename}"

        db_recipe = Recipe(
            user_id=recipe_in.user_id,
            name=recipe_in.name,
            instructions=recipe_in.instructions,
            prep_time=recipe_in.prep_time,
            cook_time=recipe_in.cook_time,
            photo=photo_path_for_db
        )

        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)

        redis_client.delete("recipes")
        return db_recipe

recipe_service = RecipeService()