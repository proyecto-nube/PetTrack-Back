from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import Base, engine, get_db
from fastapi.security import OAuth2PasswordBearer
import requests
import os

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Appointments Service")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")


def get_user(token: str = Depends(oauth2_scheme)):
    r = requests.get(f"{AUTH_SERVICE_URL}/profile", headers={"Authorization": f"Bearer {token}"})
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Token inválido")
    return r.json()


@app.post("/appointments", response_model=schemas.AppointmentResponse)
def create_appointment(appo: schemas.AppointmentBase, user=Depends(get_user), db: Session = Depends(get_db)):
    new_appo = models.Appointment(**appo.dict(), owner_id=user["id"])
    db.add(new_appo)
    db.commit()
    db.refresh(new_appo)
    return new_appo


@app.get("/appointments", response_model=list[schemas.AppointmentResponse])
def list_appointments(user=Depends(get_user), db: Session = Depends(get_db)):
    return db.query(models.Appointment).filter(models.Appointment.owner_id == user["id"]).all()
