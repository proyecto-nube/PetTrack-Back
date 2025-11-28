import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("POSTCONSULT_DATABASE_URL", "mysql+pymysql://root:password@localhost/vet_postconsultas")
    auth_service_url: str | None = os.getenv("AUTH_SERVICE_URL")
    default_points: int = int(os.getenv("FOLLOWUP_DEFAULT_POINTS", "50"))


settings = Settings()
