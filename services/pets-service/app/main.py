from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import Base, engine, get_db
from fastapi.security import OAuth2PasswordBearer
import requests
import os

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Pets Service")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")


def get_user(token: str = Depends(oauth2_scheme)):
    r = requests.get(f"{AUTH_SERVICE_URL}/profile", headers={"Authorization": f"Bearer {token}"})
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Token inválido")
    return r.json()


@app.post("/pets", response_model=schemas.PetResponse)
def create_pet(pet: schemas.PetBase, user=Depends(get_user), db: Session = Depends(get_db)):
    new_pet = models.Pet(**pet.dict(), owner_id=user["id"])
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet


@app.get("/pets", response_model=list[schemas.PetResponse])
def list_pets(user=Depends(get_user), db: Session = Depends(get_db)):
    return db.query(models.Pet).filter(models.Pet.owner_id == user["id"]).all()
