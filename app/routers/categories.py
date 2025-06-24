# app/routers/categories.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

from app.security import get_current_active_user
from app.models.user import User
from app.models.category import Category

router = APIRouter(
    prefix = "/category",
    tags = ["category"],
)

category_service = CategoryService()

@router.get('/', response_model=List[CategoryResponse])
async def index(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
   categories = category_service.get_all_categories(db)
   return categories

@router.post('/', response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def store(req: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    existing_category = db.query(Category).filter(Category.category == req.category).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    category = category_service.create_category(db, req)
    return category

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def destroy(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    deleted = category_service.destroy(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return

@router.put('/{id}', response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def update(id: int, req: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Retrieve existing category
    existing_category = db.query(Category).filter(Category.id == id).first()
    if not existing_category:
        raise HttpException(status_code=404, detail=f"Category with id {id} not found")

    updated_category = category_service.update(db, existing_category, req)

    return updated_category