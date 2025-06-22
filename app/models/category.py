# app/models/category.py
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    recipes = relationship("Recipe", secondary="recipe_categories", back_populates="categories")
    recipe_categories_link = relationship("RecipeCategory", back_populates="category", primaryjoin="Category.id == RecipeCategory.category_id", foreign_keys="[RecipeCategory.category_id]")