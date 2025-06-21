# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Recipe & Meal Planner API" # Now from .env
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "default-dev-secret" # Default if not set in .env
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # --- DATABASE SETTINGS FOR MySQL ---
    # These names should match the env vars you're passing to the container
    DB_SERVER_HOST: str # Renamed from MYSQL_SERVER for clarity in app context
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URL: str = "" # This will be constructed or directly read if available

    # Redis
    REDIS_HOST: str = "redis" # Default for local .env if not using docker-compose
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_URL: str = ""

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # AWS Bedrock
    AWS_REGION: str = "us-east-1"
    BEDROCK_MODEL_ID: str = "anthropic.claude-v2"

    # Pydantic-settings config:
    # `env_file` points to the .env file that Pydantic itself should load.
    # When running with Docker Compose, Compose handles injecting env vars from its .env
    # into the container's environment, so this part for the Dockerized app is primarily
    # for local testing *without* Docker Compose (e.g., `python -m uvicorn ...`).
    # However, it's good practice to keep it for consistency or local manual runs.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Construct DATABASE_URL if individual components are set AND DATABASE_URL is not already explicitly provided
        if self.DB_SERVER_HOST and self.DB_USER and self.DB_PASSWORD and self.DB_NAME and not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"mysql+pymysql://{self.DB_USER}:"
                f"{self.DB_PASSWORD}@{self.DB_SERVER_HOST}/{self.DB_NAME}"
            )
        # Construct REDIS_URL
        if not self.REDIS_URL:
            self.REDIS_URL = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

settings = Settings()