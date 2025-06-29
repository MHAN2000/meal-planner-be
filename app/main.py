# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session
from .config import settings
from .routers import categories, users, recipes, recipe_categories, ingredients, recipe_ingredients
from app.database.connection import get_db # Ensure this is imported
import fastapi_swagger_dark as fsd

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=None
)

router = APIRouter()
fsd.install(router, path="/")
app.include_router(router)

app.include_router(categories.router)
app.include_router(users.router)
app.include_router(recipes.router)
app.include_router(recipe_categories.router)
app.include_router(ingredients.router)
app.include_router(recipe_ingredients.router)

@app.get("/")
async def read_root():
    return {"message": "Hello Worlds"}

@app.get('/health/db', summary="Check database connection health")
async def check_db_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1")) # Use db.execute(text("SELECT 1")) if you are using SQLAlchemy 2.0 style
        return {"status": "Database connection successful!"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {e}"
        )