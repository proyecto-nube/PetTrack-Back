from pydantic import BaseModel
from datetime import datetime

class AppointmentBase(BaseModel):
    pet_name: str
    owner_name: str
    doctor_name: str
    reason: str
    date: datetime | None = None

class AppointmentResponse(AppointmentBase):
    id: int
    class Config:
        orm_mode = True
