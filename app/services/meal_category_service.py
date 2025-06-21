# app/services/meal_category_service.py
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.meal_category import MealCategory
from app.schemas.meal_category import MealCategoryCreate, MealCategoryUpdate

class MealCategoryService:
    def get_all_meal_categories(self, db: Session) -> list[MealCategory]:
        query = select(MealCategory)
        data = db.scalars(query).all()
        return data
