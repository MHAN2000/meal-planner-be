from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class RecipeCategory(Base):
    __tablename__ = "recipe_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    # Foreign Key to Recipe id
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    # Foreign Key to Meal Category id
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    recipe = relationship("Recipe", back_populates="recipe_categories_link")
    category = relationship("Category", back_populates="recipe_categories_link")