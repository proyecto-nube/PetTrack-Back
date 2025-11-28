from dotenv import load_dotenv
import os
from functools import lru_cache
from pymongo import MongoClient
from pymongo.errors import ConfigurationError

load_dotenv()

COSMOS_DB_URI = os.getenv("COSMOS_MONGO_URL")
COSMOS_DB_NAME = os.getenv("DATABASE_NAME", "rewards_db")


@lru_cache
def _get_db():
    """Inicializa la conexión solo cuando se necesita."""
    if not COSMOS_DB_URI:
        raise ConfigurationError("COSMOS_MONGO_URL no está configurada.")
    client = MongoClient(COSMOS_DB_URI)
    return client[COSMOS_DB_NAME]


def get_collection(name: str):
    """Devuelve una colección por nombre."""
    return _get_db()[name]
