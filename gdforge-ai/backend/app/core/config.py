from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Konfigurační třída aplikace"""

    # API klíče
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # LLM model
    llm_provider: str = "openai"  # "openai" nebo "anthropic"
    llm_model: str = "gpt-4-turbo-preview"

    # Nastavení aplikace
    app_title: str = "GDForge AI"
    app_version: str = "0.1.0"
    app_description: str = "Infrastructure as Code pro Godot herní vývoj"
    debug: bool = False

    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    model_config = ConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    """Vrací globální instanci nastavení"""
    return Settings()


settings = get_settings()
