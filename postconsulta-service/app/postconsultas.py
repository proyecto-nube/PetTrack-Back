from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import postconsulta_crud, postconsulta_schema

router = APIRouter(prefix="/postconsultas", tags=["PostConsultas"])

@router.get("/", response_model=list[postconsulta_schema.PostConsultaResponse])
def listar_postconsultas(db: Session = Depends(get_db)):
    return postconsulta_crud.get_postconsultas(db)

@router.get("/{postconsulta_id}", response_model=postconsulta_schema.PostConsultaResponse)
def obtener_postconsulta(postconsulta_id: int, db: Session = Depends(get_db)):
    postconsulta = postconsulta_crud.get_postconsulta(db, postconsulta_id)
    if not postconsulta:
        raise HTTPException(status_code=404, detail="Postconsulta no encontrada")
    return postconsulta

@router.post("/", response_model=postconsulta_schema.PostConsultaResponse)
def crear_postconsulta(postconsulta: postconsulta_schema.PostConsultaCreate, db: Session = Depends(get_db)):
    return postconsulta_crud.create_postconsulta(db, postconsulta)

@router.put("/{postconsulta_id}", response_model=postconsulta_schema.PostConsultaResponse)
def actualizar_postconsulta(postconsulta_id: int, update_data: postconsulta_schema.PostConsultaUpdate, db: Session = Depends(get_db)):
    updated = postconsulta_crud.update_postconsulta(db, postconsulta_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Postconsulta no encontrada")
    return updated

@router.delete("/{postconsulta_id}")
def eliminar_postconsulta(postconsulta_id: int, db: Session = Depends(get_db)):
    deleted = postconsulta_crud.delete_postconsulta(db, postconsulta_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Postconsulta no encontrada")
    return {"message": "Postconsulta eliminada correctamente"}
