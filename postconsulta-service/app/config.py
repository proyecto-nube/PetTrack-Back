# ✅ Import correcto en Pydantic v2
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "postconsulta-service"
    DATABASE_URL: str
    PORT: int = 8004

    class Config:
        env_file = ".env"

settings = Settings()
