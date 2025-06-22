from sqlalchemy import Column, Integer, String, func, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    ingredient = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    recipes = relationship("Recipe", secondary="recipe_ingredients", back_populates="ingredients")
    ingredients_link = relationship("RecipeIngredient", back_populates="ingredient", primaryjoin="Ingredient.id == RecipeIngredient.ingredient_id", foreign_keys="[RecipeIngredient.ingredient_id]")
    shopping_cart = relationship("ShoppingCart", back_populates="ingredient")
