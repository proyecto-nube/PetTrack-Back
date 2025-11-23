from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    pet_name = Column(String(100))
    owner_name = Column(String(100))
    doctor_name = Column(String(100))
    date = Column(DateTime, default=datetime.utcnow)
    reason = Column(String(255))
