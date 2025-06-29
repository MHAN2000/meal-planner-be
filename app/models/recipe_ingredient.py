from sqlalchemy import Column, ForeignKey, Integer, String, func, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base

class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    qty = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    #Relationships
    ingredient = relationship("Ingredient", back_populates="ingredients_link")
    recipe = relationship("Recipe", back_populates="recipe_ingredients_link")

