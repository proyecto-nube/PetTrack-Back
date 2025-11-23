import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("POSTCONSULT_APP_NAME")
    APP_ENV = os.getenv("POSTCONSULT_APP_ENV")
    PORT = os.getenv("POSTCONSULT_PORT")

    DATABASE_URL = os.getenv("POSTCONSULT_DATABASE_URL")

settings = Settings()
