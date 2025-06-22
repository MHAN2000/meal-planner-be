# app/services/category_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List
import json

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.redis_client import redis_client
from app.config import settings

class CategoryService:
    def get_all_categories_from_db(self, db: Session) -> List[Category]:
        return db.scalars(select(Category).where(Category.deleted_at.is_(None))).all()

    def get_all_categories(self, db: Session) -> List[Category]:
        # 1. Try to get data from redis if it exists
        cached_data = redis_client.get("categories")
        if cached_data:
            print("DEBUG: Cache hit for categories")
            return [Category(**item) for item in json.loads(cached_data)]

        print("DEBUG: Cache miss for categories, fetching from db")

        # 2. If it is not in redis, fetch categories from db
        categories = self.get_all_categories_from_db(db)
        # 3. Save in redis and set an expiration time
        categories_response_data = [CategoryResponse.model_validate(c).model_dump(mode='json') for c in categories]
        # 4. Serialize the objects list to JSON and save it into redis
        redis_client.setex("categories", settings.REDIS_CACHE_EXPIRE_SECONDS, json.dumps(categories_response_data))

        return categories

    def update(self, db: Session, db_category: Category, req: CategoryUpdate) -> Category:
        update_data = req.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)

        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        redis_client.delete("categories")

        return db_category


    def destroy(self, db: Session, id: int) -> bool:
        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            return False # Category not found

        # Update the deleted_at timestamp
        category.deleted_at = func.now()
        category.is_active = False

        db.add(category)
        db.commit()
        db.refresh(category)

        # Invalidate the redis cache
        redis_client.delete("categories")

        return True

    def create_category(self, db: Session, req: CategoryCreate) -> Category:
        db_category = Category(**req.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        redis_client.delete("categories")
        return db_category

