from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./kuadra_reset.db")
    ENV: str = os.getenv("ENV", "development")


settings = Settings()

print("DATABASE_URL =", settings.DATABASE_URL)
