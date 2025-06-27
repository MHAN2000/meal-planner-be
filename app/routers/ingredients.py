from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional, Union

from app.database.connection import get_db
from app.schemas.ingredient import IngredientResponse, IngredientCreate, IngredientUpdate
from app.services.ingredient_service import IngredientService

from app.security import get_current_active_user
from app.models.ingredient import Ingredient
from app.models.user import User

router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
)

ingredient_service = IngredientService()

@router.get("/", response_model=List[IngredientResponse])
async def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    ingredients = ingredient_service.get_all_ingredients(db)
    return ingredients