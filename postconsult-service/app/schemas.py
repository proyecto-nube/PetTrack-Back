from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

FollowUpStatus = Literal["Pendiente", "Enviado recordatorio", "Completado", "Cancelado"]


class FollowUpBase(BaseModel):
    pet_name: str = Field(..., description="Nombre de la mascota")
    owner_name: str = Field(..., description="Nombre del tutor")
    type: str = Field(..., description="Tipo de seguimiento")
    date: str = Field(..., description="Fecha YYYY-MM-DD")
    time: str = Field(..., description="Hora HH:MM")
    status: FollowUpStatus = "Pendiente"
    notes: Optional[str] = None
    points_on_complete: int = Field(50, alias="pointsOnComplete")
    owner_id: Optional[str] = Field(default=None, description="ID del dueño (opcional)")
    created_by: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class FollowUpCreate(FollowUpBase):
    pass


class FollowUpUpdate(BaseModel):
    status: Optional[FollowUpStatus] = None
    notes: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

    class Config:
        allow_population_by_field_name = True


class FollowUpResponse(FollowUpBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
