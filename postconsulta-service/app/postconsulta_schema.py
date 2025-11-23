from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class PostConsultaBase(BaseModel):
    mascota_id: int
    veterinario_id: int
    diagnostico: str
    tratamiento: Optional[str] = None
    observaciones: Optional[str] = None
    proxima_cita: Optional[datetime] = None
    estado: Optional[Literal["pendiente", "completada", "cancelada"]] = "pendiente"

class PostConsultaCreate(PostConsultaBase):
    pass

class PostConsultaUpdate(PostConsultaBase):
    pass

class PostConsultaResponse(PostConsultaBase):
    id: int
    fecha_consulta: datetime

    class Config:
        orm_mode = True
