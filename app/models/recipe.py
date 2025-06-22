from sqlalchemy import Column, Integer, func, DateTime, String, Text, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    # Foreign Key to Users table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String(50), nullable=False)
    instructions = Column(Text, nullable=False)
    prep_time = Column(SmallInteger, nullable=False)
    cook_time = Column(SmallInteger, nullable=False)
    photo = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="recipes")
    categories = relationship("Category", secondary="recipe_categories", back_populates="recipes")
    recipe_categories_link = relationship(
        "RecipeCategory", back_populates="recipe", primaryjoin="Recipe.id == RecipeCategory.recipe_id", foreign_keys="[RecipeCategory.recipe_id]"
    )
    recipe_ingredients_link = relationship("RecipeIngredient", back_populates="recipe", primaryjoin="Recipe.id == RecipeIngredient.recipe_id", foreign_keys="[RecipeIngredient.recipe_id]")