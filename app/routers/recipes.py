# app/routers/recipes.py
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional, Union

from app.database.connection import get_db
from app.schemas.recipe import RecipeResponse, RecipeCreate, RecipeUpdate
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
    recipe_create_data = RecipeCreate(user_id=current_user.id, name=name, instructions=instructions,
                                      prep_time=prep_time, cook_time=cook_time)
    file_content_bytes = await photo.read()
    file_original_name = photo.filename

    recipe = recipe_service.create_recipe(db=db, recipe_in=recipe_create_data, photo_file_bytes=file_content_bytes,
                                          photo_filename=file_original_name)

    return recipe


@router.put("/{id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK)
async def update(id: int,
                 name: Optional[str] = Form(None),
                 instructions: Optional[str] = Form(None),
                 prep_time: Optional[int] = Form(None),
                 cook_time: Optional[int] = Form(None),
                 photo: Optional[Union[UploadFile, str]] = File(None),
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_active_user)
                 ):
    file_content_bytes = None
    file_original_name = None
    if photo and photo.filename:
        file_content_bytes = await photo.read()
        file_original_name = photo.filename

    existing_recipe = db.query(Recipe).filter(Recipe.id == id).first()

    if not existing_recipe:
        raise HttpException(status_code=404, detail=f"Recipe with id {id} not found")

    recipe_update_data = RecipeUpdate(user_id=current_user.id, name=name, instructions=instructions,
                                      prep_time=prep_time, cook_time=cook_time)

    updated_recipe = recipe_service.update_recipe(db, existing_recipe, recipe_update_data, photo_file_bytes=file_content_bytes,
                                           photo_filename=file_original_name)

    return updated_recipe

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted = recipe_service.destroy(db, id)
    if not deleted:
        raise HttpException(status_code=404, detail=f"Recipe with id {id} not found")

    return
