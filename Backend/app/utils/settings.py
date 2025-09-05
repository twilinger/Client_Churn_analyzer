from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / ".env", extra="ignore")

    APP_TITLE: str = "Churn Analyzer API"
    APP_VERSION: str = "0.1.0"

    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b"

    VECTOR_DB_PATH: str | None = None   
    TOP_K: int = 4

settings = Settings()
