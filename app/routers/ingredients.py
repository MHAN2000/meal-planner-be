from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy import select
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

@router.post("/", response_model=IngredientResponse, status_code=status.HTTP_201_CREATED)
async def store(req: IngredientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    existing_ingredient = db.scalars(select(Ingredient).where(Ingredient.ingredient == req.ingredient)).first()
    if existing_ingredient:
        return HTTPException(status_code=400, detail="ingredient already exists")

    ingredient = ingredient_service.create_ingredient(db, req)
    return ingredient

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted = ingredient_service.destroy(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Ingredient with id {id} not found")
    return

@router.put('/{id}', response_model=IngredientResponse, status_code=status.HTTP_200_OK)
async def update(id: int, req: IngredientUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Retrieve existing ingredient
    ingredient = db.scalars(select(Ingredient).where(Ingredient.id == id)).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail=f"Ingredient with id {id} not found")

    updated_ingredient = ingredient_service.update(db, ingredient, req)

    return updated_ingredient