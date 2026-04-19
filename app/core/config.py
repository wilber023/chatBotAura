from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Aura AI Agent"
    VERSION: str = "3.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # Security
    API_KEY_SECRET: str = "super_secret_default_key" # Change in production
    
    # AI Models Config
    SENTIMENT_MODEL_NAME: str = "UMUTeam/roberta-spanish-sentiment-analysis"
    LLM_MODEL_NAME: str = "HuggingFaceH4/zephyr-7b-beta" # Example for future use
    HF_TOKEN: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "sqlite:///./aura.db"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    """Retorna una instancia cacheada de la configuración"""
    return Settings()
