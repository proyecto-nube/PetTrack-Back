from sqlalchemy import Column, Integer, String
from .database import Base

# --- Modelos de la base de datos ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role = Column(String(20), nullable=False)  # 'user', 'doctor', 'admin'
