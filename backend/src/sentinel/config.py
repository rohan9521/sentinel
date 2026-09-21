from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings for the backend."""

    app_name: str = "sentinel"
    llm_provider: str = Field(default="fake", validation_alias="SENTINEL_LLM_PROVIDER")
    model_name: str = Field(default="fake-model", validation_alias="SENTINEL_MODEL_NAME")
    max_usd: float = Field(default=0.25, validation_alias="SENTINEL_MAX_USD")
    seed: int = Field(default=42, validation_alias="SENTINEL_SEED")
    api_host: str = Field(default="0.0.0.0", validation_alias="SENTINEL_API_HOST")
    api_port: int = Field(default=8000, validation_alias="SENTINEL_API_PORT")

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SENTINEL_", case_sensitive=False)


settings = Settings()

