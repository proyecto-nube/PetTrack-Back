from sqlalchemy.orm import Session
from app import postconsulta_model, postconsulta_schema

def get_postconsultas(db: Session):
    return db.query(postconsulta_model.PostConsulta).all()

def get_postconsulta(db: Session, postconsulta_id: int):
    return db.query(postconsulta_model.PostConsulta).filter(
        postconsulta_model.PostConsulta.id == postconsulta_id
    ).first()

def create_postconsulta(db: Session, postconsulta: postconsulta_schema.PostConsultaCreate):
    db_postconsulta = postconsulta_model.PostConsulta(**postconsulta.dict())
    db.add(db_postconsulta)
    db.commit()
    db.refresh(db_postconsulta)
    return db_postconsulta

def update_postconsulta(db: Session, postconsulta_id: int, update_data: postconsulta_schema.PostConsultaUpdate):
    db_postconsulta = get_postconsulta(db, postconsulta_id)
    if db_postconsulta:
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(db_postconsulta, key, value)
        db.commit()
        db.refresh(db_postconsulta)
    return db_postconsulta

def delete_postconsulta(db: Session, postconsulta_id: int):
    db_postconsulta = get_postconsulta(db, postconsulta_id)
    if db_postconsulta:
        db.delete(db_postconsulta)
        db.commit()
    return db_postconsulta
