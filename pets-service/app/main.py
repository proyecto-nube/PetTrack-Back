from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .database import Base, engine, get_db, SessionLocal
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

@app.put("/pets/{pet_id}", response_model=schemas.PetResponse)
def update_pet(pet_id: int, pet: schemas.PetBase, user=Depends(get_user), db: Session = Depends(get_db)):
    db_pet = db.query(models.Pet).filter(models.Pet.id == pet_id, models.Pet.owner_id == user["id"]).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    for key, value in pet.dict().items():
        setattr(db_pet, key, value)
    db.commit()
    db.refresh(db_pet)
    return db_pet

@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int, user=Depends(get_user), db: Session = Depends(get_db)):
    db_pet = db.query(models.Pet).filter(models.Pet.id == pet_id, models.Pet.owner_id == user["id"]).first()
    if not db_pet:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    db.delete(db_pet)
    db.commit()
    return {"detail": "Mascota eliminada"}

@app.get("/health")
def health():
    return {"status": "Pets service is healthy"}

@app.get("/")
def root():
    return {"message": "Welcome to the Pets Service"}


@app.on_event("startup")
def startup_event():
    print("Pets service started correctly inside Azure Container")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Azure define PORT automáticamente
    uvicorn.run(app, host="0.0.0.0", port=port)