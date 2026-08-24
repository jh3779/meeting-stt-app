from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str = ""
    firestore_service_account_path: str = "serviceAccountKey.json"
    max_input_chars: int = 20_000


@lru_cache
def get_settings() -> Settings:
    return Settings()
