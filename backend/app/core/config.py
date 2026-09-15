import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "ARTINO Platform API"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./artino.db")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "artino_hackathon_demo_secret_2026")
    
    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
