from sqlalchemy import Column, Integer, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class ShoppingCart(Base):
    __tablename__ = "shopping_cart"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    qty = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="shopping_cart")
    ingredient = relationship("Ingredient", back_populates="shopping_cart")