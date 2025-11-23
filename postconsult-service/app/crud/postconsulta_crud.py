from sqlalchemy.orm import Session
from app import models as postconsulta_model
from app import schemas as postconsulta_schema


# 🔹 Obtener TODAS las postconsultas (doctor/admin)
def get_postconsultas(db: Session):
    return db.query(postconsulta_model.PostConsulta).all()


# 🔹 Obtener postconsultas SOLO del dueño
def get_postconsultas_by_owner(db: Session, owner_id: int):
    return (
        db.query(postconsulta_model.PostConsulta)
        .filter(postconsulta_model.PostConsulta.owner_id == owner_id)
        .all()
    )


# 🔹 Obtener una sola postconsulta por ID
def get_postconsulta(db: Session, postconsulta_id: int):
    return (
        db.query(postconsulta_model.PostConsulta)
        .filter(postconsulta_model.PostConsulta.id == postconsulta_id)
        .first()
    )


# 🔹 Crear postconsulta → doctor/admin (agrega owner automáticamente)
def create_postconsulta(db: Session, postconsulta: postconsulta_schema.PostConsultaCreate, owner_id: int):
    db_postconsulta = postconsulta_model.PostConsulta(
        **postconsulta.dict(),
        owner_id=owner_id  # Asignar quién la creó
    )
    db.add(db_postconsulta)
    db.commit()
    db.refresh(db_postconsulta)
    return db_postconsulta


# 🔹 Actualizar postconsulta (solo doctor/admin)
def update_postconsulta(db: Session, postconsulta_id: int, update_data: postconsulta_schema.PostConsultaUpdate):
    db_postconsulta = get_postconsulta(db, postconsulta_id)
    if db_postconsulta:
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(db_postconsulta, key, value)

        db.commit()
        db.refresh(db_postconsulta)

    return db_postconsulta


# 🔹 Eliminar → solo admin
def delete_postconsulta(db: Session, postconsulta_id: int):
    db_postconsulta = get_postconsulta(db, postconsulta_id)
    if db_postconsulta:
        db.delete(db_postconsulta)
        db.commit()
    return db_postconsulta
