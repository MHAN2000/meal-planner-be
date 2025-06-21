# app/models/meal_category.py
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from app.database.connection import Base # Import your Base

class MealCategory(Base):
    __tablename__ = "meal_categories"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Add relationships if needed (e.g., recipes created by user)
    # recipes = relationship("Recipe", back_populates="owner")