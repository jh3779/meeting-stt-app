from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# .env의 LANGCHAIN_* 값(트레이싱 켜기)은 우리 Settings에 선언되지 않은 필드라
# pydantic-settings만으로는 os.environ에 반영되지 않는다 — LangChain/LangSmith가
# os.environ을 직접 읽으므로 load_dotenv()로 프로세스 환경 전체에 로드해준다.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    firestore_service_account_path: str = "serviceAccountKey.json"
    max_input_chars: int = 20_000


@lru_cache
def get_settings() -> Settings:
    return Settings()
