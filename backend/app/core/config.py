"""Runtime settings loaded from environment variables."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "E-Waste Advisor API"
    environment: str = "development"
    max_upload_size_mb: int = 10
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    demo_data_path: str = "../data/recyclers.csv"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ewaste_advisor"
    secret_key: str = "change-me-in-production"
    session_expiry_hours: int = 24
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
