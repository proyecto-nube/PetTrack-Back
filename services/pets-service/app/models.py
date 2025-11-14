from sqlalchemy import Column, Integer, String
from .database import Base

class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    species = Column(String(100))
    breed = Column(String(100))
    owner_name = Column(String(100))
