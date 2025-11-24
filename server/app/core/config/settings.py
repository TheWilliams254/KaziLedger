from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = ConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../../.env"),
        env_file_encoding="utf-8"
    )

settings = Settings()

# print(settings.DATABASE_URL)