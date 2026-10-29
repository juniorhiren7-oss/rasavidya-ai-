from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RASAVIDYA AI"
    app_env: str = "development"
    database_url: str = "sqlite:///./rasavidya.db"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    admin_api_token: str = ""
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    max_research_task_chars: int = 4000

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
