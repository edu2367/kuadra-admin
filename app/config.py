from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./kuadra_reset.db"


settings = Settings()

print("DATABASE_URL =", settings.DATABASE_URL)
