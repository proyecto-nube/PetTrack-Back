from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text

from .database import Base


class PostConsultFollowUp(Base):
    __tablename__ = "vet_postconsultas"

    id = Column(Integer, primary_key=True, index=True)
    pet_name = Column(String(120), nullable=False)
    owner_name = Column(String(120), nullable=False)
    type = Column(String(160), nullable=False)
    date = Column(String(20), nullable=False)
    time = Column(String(20), nullable=False)
    status = Column(String(40), nullable=False, default="Pendiente")
    notes = Column(Text, nullable=True)
    points_on_complete = Column(Integer, nullable=False, default=50)
    owner_id = Column(String(64), nullable=True, index=True)
    created_by = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

