from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    app_name: str = "Auth API"
    debug: bool = False

    # Security
    secret_key: str = "CHANGE_ME"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Fake "database" for this simple example
    # In a real project you would define proper DB settings here

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"

