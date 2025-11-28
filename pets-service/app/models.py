from sqlalchemy import Column, Integer, String
from .database import Base

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    species = Column(String(100), nullable=False)
    breed = Column(String(100), nullable=True)

    # 🔗 Relación lógica con auth-service (usuario), pero sin ORM
    owner_name = Column(String(100), nullable=False)  # backup o referencia visual
    owner_id = Column(Integer, nullable=False, index=True)  # ID del user en auth-service

    # (Opcional si quieres que MySQL lo valide como FK aunque SQLAlchemy no lo use)
    # owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
