from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Cargar variables desde .env
DATABASE_URL = os.getenv("DATABASE_URL")
SSL_CA = os.getenv("DB_SSL_CA")

# Forzar SSL si no estaba incluido
if "ssl_ca" not in DATABASE_URL:
    DATABASE_URL += f"?ssl_ca={SSL_CA}&ssl_verify_cert=true"

# Crear engine con configuraciones necesarias para Azure
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=280,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
