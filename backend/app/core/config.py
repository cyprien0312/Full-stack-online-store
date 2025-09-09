from functools import lru_cache
from pydantic import BaseModel
import os


class Settings(BaseModel):
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://app:app@127.0.0.1:5432/app",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


