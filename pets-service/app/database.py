from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_HOST = os.getenv("DB_HOST", "pettrack-mysql.mysql.database.azure.com")
DB_NAME = os.getenv("DB_NAME")  # cambia por cada microservicio
DB_USER = os.getenv("DB_USER", "adminpet")
DB_PASSWORD = os.getenv("DB_PASSWORD", "PetTrack2025")
SSL_CA = os.path.join(os.path.dirname(__file__), "../DigiCertGlobalRootG2.pem")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
    f"?ssl_ca={SSL_CA}&ssl_verify_cert=true"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()