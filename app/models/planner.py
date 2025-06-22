from sqlalchemy import Column, Integer, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Planner(Base):
    __tablename__ = "planner"

    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="planners")
    recipe = relationship("Recipe", back_populates="planners")