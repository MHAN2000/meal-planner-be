# app/routers/recipes.py
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.connection import get_db
from app.schemas.recipe import RecipeResponse, RecipeCreate
from app.services.recipe_service import RecipeService

from app.security import get_current_active_user
from app.models.recipe import Recipe
from app.models.user import User

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)

recipe_service = RecipeService()


@router.get("/", response_model=List[RecipeResponse])
async def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    recipes = recipe_service.get_recipes(db)
    return recipes


@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def store(
        name: str = Form(...),
        instructions: str = Form(...),
        prep_time: int = Form(...),
        cook_time: int = Form(...),
        photo: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):

    recipe_create_data = RecipeCreate(user_id=current_user.id, name=name, instructions=instructions, prep_time=prep_time, cook_time=cook_time)
    file_content_bytes = await photo.read()
    file_original_name = photo.filename

    recipe = recipe_service.create_recipe(db=db, recipe_in=recipe_create_data, photo_file_bytes=file_content_bytes, photo_filename=file_original_name)

    return recipe
