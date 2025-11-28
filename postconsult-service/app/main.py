from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import requests

from .config import settings
from . import schemas, crud, models
from .database import Base, engine, get_db

app = FastAPI(title="Postconsult Follow-ups Service", version="1.1")

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(token: str = Depends(oauth2_scheme)):
    if not settings.auth_service_url:
        raise HTTPException(status_code=500, detail="AUTH_SERVICE_URL no configurada")

    try:
        response = requests.get(
            f"{settings.auth_service_url}/profile",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
    except requests.RequestException as exc:
        raise HTTPException(status_code=503, detail="Auth service no disponible") from exc

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Token inválido")
    return response.json()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _to_response(entity: models.PostConsultFollowUp) -> dict:
    return schemas.FollowUpResponse.model_validate(entity).model_dump(by_alias=True)


@app.get("/followups", response_model=list[schemas.FollowUpResponse])
def list_followups(user=Depends(get_user), db: Session = Depends(get_db)):
    owner_filter = None
    if user.get("role") == "owner":
        owner_filter = str(user["id"])

    followups = crud.list_followups(db, owner_filter)
    return [_to_response(f) for f in followups]


@app.post("/followups", response_model=schemas.FollowUpResponse, status_code=status.HTTP_201_CREATED)
def create_followup(
    payload: schemas.FollowUpCreate,
    user=Depends(get_user),
    db: Session = Depends(get_db),
):
    if user.get("role") not in ["doctor", "admin"]:
        raise HTTPException(status_code=403, detail="Solo personal médico puede crear seguimientos")

    payload.points_on_complete = payload.points_on_complete or settings.default_points
    entity = crud.create_followup(db, payload, str(user["id"]))
    return _to_response(entity)


@app.patch("/followups/{followup_id}", response_model=schemas.FollowUpResponse)
def update_followup(
    followup_id: int,
    payload: schemas.FollowUpUpdate,
    user=Depends(get_user),
    db: Session = Depends(get_db),
):
    entity = crud.get_followup(db, followup_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")

    if user.get("role") == "owner" and entity.owner_id not in (None, str(user["id"])):
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar este seguimiento")

    updated = crud.update_followup(db, entity, payload)
    return _to_response(updated)


@app.get("/health")
def health():
    return {"service": "postconsult-service", "status": "ok"}


@app.get("/")
def root():
    return {"message": "Servicio de Seguimiento Post-Consulta activo 🚀"}
