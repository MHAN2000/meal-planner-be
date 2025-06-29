from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import select

from app.database.connection import get_db
from app.schemas.recipe_ingredient import RecipeIngredientResponse, RecipeIngredientCreate, RecipeIngredientUpdate
from app.services.recipe_ingredient_service import RecipeIngredientService

from app.security import get_current_active_user
from app.models.recipe_ingredient import RecipeIngredient
from app.models.user import User

router = APIRouter(
    prefix="/recipe_ingredients",
    tags=["recipe_ingredients"]
)

recipe_ingredient_service = RecipeIngredientService()

@router.get('/', response_model=List[RecipeIngredientResponse])
async def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    recipe_ingredients = recipe_ingredient_service.get_all_recipe_ingredients(db)
    return recipe_ingredients;

@router.post('/', response_model=RecipeIngredientResponse, status_code=status.HTTP_201_CREATED)
async def store(req: RecipeIngredientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    recipe_ingredient = recipe_ingredient_service.create_recipe_ingredient(db, req)
    return recipe_ingredient

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db : Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted = recipe_ingredient_service.delete_recipe_ingredient(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Recipe with id {id} not found")
    return

@router.put('/{id}', response_model=RecipeIngredientResponse, status_code=status.HTTP_200_OK)
async def update(id: int, req: RecipeIngredientUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    existing_recipe_ingredient = db.scalars(select(RecipeIngredient).where(RecipeIngredient.id == id)).first()
    if not existing_recipe_ingredient:
        raise HTTPException(status_code=404, detail=f"Recipe with id {id} not found")

    update_recipe_ingredient = recipe_ingredient_service.update(db, existing_recipe_ingredient, req)

    return update_recipe_ingredient