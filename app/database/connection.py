# app/database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is for SQLite; remove for PostgreSQL if not needed.
engine = create_engine(settings.DATABASE_URL)

# Create a SessionLocal class to get a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()