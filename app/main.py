# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from .config import settings
from .routers import meal_category, users
from app.database.connection import get_db # Ensure this is imported

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(meal_category.router)
app.include_router(users.router)

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