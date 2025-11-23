from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import postconsulta_crud
from app import schemas as postconsulta_schema

router = APIRouter(prefix="/postconsultas", tags=["PostConsultas"])


# ───────────────────────────────
# 🔹 GET → Dueño ve solo sus registros
# 🔹 GET → Doctor/Admin ven todos
# ───────────────────────────────
@router.get("/", response_model=list[postconsulta_schema.PostConsultaResponse])
def listar_postconsultas(
    db: Session = Depends(get_db),
    user=Depends(lambda: None)
):
    role = user["role"]

    if role == "user":
        return postconsulta_crud.get_postconsultas_by_owner(db, user["id"])

    if role in ["doctor", "admin"]:
        return postconsulta_crud.get_postconsultas(db)


@router.get("/{postconsulta_id}", response_model=postconsulta_schema.PostConsultaResponse)
def obtener_postconsulta(
    postconsulta_id: int,
    db: Session = Depends(get_db),
    user=Depends(lambda: None)
):
    pc = postconsulta_crud.get_postconsulta(db, postconsulta_id)
    if not pc:
        raise HTTPException(status_code=404, detail="Postconsulta no encontrada")

    if user["role"] == "user" and pc.owner_id != user["id"]:
        raise HTTPException(status_code=403, detail="No puedes ver esta postconsulta")

    return pc


# ───────────────────────────────
# 🔹 POST → Solo doctor/admin
# ───────────────────────────────
@router.post("/", response_model=postconsulta_schema.PostConsultaResponse)
def crear_postconsulta(
    postconsulta: postconsulta_schema.PostConsultaCreate,
    db: Session = Depends(get_db),
    user=Depends(lambda: None)
):
    if user["role"] not in ["doctor", "admin"]:
        raise HTTPException(status_code=403, detail="No autorizado para crear postconsultas")

    return postconsulta_crud.create_postconsulta(db, postconsulta, user["id"])


# ───────────────────────────────
# 🔹 PUT → Doctor/Admin
# ───────────────────────────────
@router.put("/{postconsulta_id}", response_model=postconsulta_schema.PostConsultaResponse)
def actualizar_postconsulta(
    postconsulta_id: int,
    update_data: postconsulta_schema.PostConsultaUpdate,
    db: Session = Depends(get_db),
    user=Depends(lambda: None)
):
    if user["role"] not in ["doctor", "admin"]:
        raise HTTPException(status_code=403, detail="No autorizado para actualizar")

    updated = postconsulta_crud.update_postconsulta(db, postconsulta_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Postconsulta no encontrada")
    return updated


# ───────────────────────────────
# 🔹 DELETE → Solo admin
# ───────────────────────────────
@router.delete("/{postconsulta_id}")
def eliminar_postconsulta(
    postconsulta_id: int,
    db: Session = Depends(get_db),
    user=Depends(lambda: None)
):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Solo admin puede eliminar")

    deleted = postconsulta_crud.delete_postconsulta(db, postconsulta_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Postconsulta no encontrada")
    return {"message": "Postconsulta eliminada correctamente"}
