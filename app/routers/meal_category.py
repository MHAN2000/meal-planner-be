# app/routers/meal_category.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.services.meal_category_service import MealCategoryService
from app.schemas.meal_category import MealCategoryCreate, MealCategoryResponse, MealCategoryUpdate

from app.security import get_current_active_user
from app.models.user import User

router = APIRouter(
    prefix = "/meal_category",
    tags = ["meal_category"],
)

meal_category_service = MealCategoryService()

@router.get('/', response_model=List[MealCategoryResponse])
async def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
   categories = meal_category_service.get_all_meal_categories(db);
   return categories
