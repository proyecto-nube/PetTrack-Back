from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

COSMOS_DB_URI = os.getenv("COSMOS_MONGO_URL")
COSMOS_DB_NAME = os.getenv("DATABASE_NAME")

# Conexión al cliente
client = MongoClient(COSMOS_DB_URI)
db = client[COSMOS_DB_NAME]


def get_collection(name: str):
    """Devuelve una colección por nombre."""
    return db[name]
