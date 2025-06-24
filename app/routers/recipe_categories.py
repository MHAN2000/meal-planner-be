from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database.connection import get_db
from app.schemas.recipe_category import RecipeCategoryCreate, RecipeCategoryUpdate, RecipeCategoryResponse
from app.services.recipe_category_service import RecipeCategoryService

from app.security import get_current_active_user
from app.models.recipe_category import RecipeCategory
from app.models.user import User

router = APIRouter(
    prefix="/recipe_categories",
    tags=["recipe_categories"]
)

recipe_category_service = RecipeCategoryService()

@router.get('/', response_model=List[RecipeCategoryResponse])
async def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    recipe_categories = recipe_category_service.get_all_recipe_categories(db)
    return recipe_categories

@router.post('/', response_model=RecipeCategoryResponse, status_code=status.HTTP_201_CREATED)
async def store(req: RecipeCategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    recipe_category = recipe_category_service.create_recipe_category(db, req)
    return recipe_category

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted = recipe_category_service.destroy(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Recipe category with id {id} not found")
    return

@router.put('/{id}', response_model=RecipeCategoryResponse, status_code=status.HTTP_200_OK)
async def update(id: int, req: RecipeCategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    existing_recipe_category = db.scalars(select(RecipeCategory).where(RecipeCategory.id == id)).first()
    if not existing_recipe_category:
        raise HTTPException(status_code=404, detail=f"Recipe category with id {id} not found")

    updated_recipe_category = recipe_category_service.update(db, existing_recipe_category, req)

    return updated_recipe_category
