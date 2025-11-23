from sqlalchemy import Column, Integer, Text, DateTime, Enum
from app.database import Base
from datetime import datetime
import enum

class EstadoConsulta(str, enum.Enum):
    pendiente = "pendiente"
    completada = "completada"
    cancelada = "cancelada"

class PostConsulta(Base):
    __tablename__ = "postconsultas"

    id = Column(Integer, primary_key=True, index=True)
    mascota_id = Column(Integer, index=True, nullable=False)
    veterinario_id = Column(Integer, index=True, nullable=False)
    fecha_consulta = Column(DateTime, default=datetime.utcnow)
    diagnostico = Column(Text, nullable=False)
    tratamiento = Column(Text, nullable=True)
    observaciones = Column(Text, nullable=True)
    proxima_cita = Column(DateTime, nullable=True)
    estado = Column(Enum(EstadoConsulta), default=EstadoConsulta.pendiente)
