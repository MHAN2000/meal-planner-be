# app/routers/meal_category.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.services.meal_category_service import MealCategoryService
from app.schemas.meal_category import MealCategoryCreate, MealCategoryResponse, MealCategoryUpdate

router = APIRouter(
    prefix = "/meal_category",
    tags = ["meal_category"],
)

meal_category_service = MealCategoryService()

@router.get('/', response_model=List[MealCategoryResponse])
async def index(db: Session = Depends(get_db)):
   categories = meal_category_service.get_all_meal_categories(db);
   return categories
