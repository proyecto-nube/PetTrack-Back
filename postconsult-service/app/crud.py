from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from . import models, schemas


def list_followups(db: Session, owner_id: Optional[str] = None):
    query = db.query(models.PostConsultFollowUp)
    if owner_id:
        query = query.filter(models.PostConsultFollowUp.owner_id == owner_id)
    return query.order_by(models.PostConsultFollowUp.date.asc()).all()


def get_followup(db: Session, followup_id: int):
    return db.query(models.PostConsultFollowUp).filter(models.PostConsultFollowUp.id == followup_id).first()


def create_followup(db: Session, payload: schemas.FollowUpCreate, creator_id: str):
    entity = models.PostConsultFollowUp(
        pet_name=payload.pet_name,
        owner_name=payload.owner_name,
        type=payload.type,
        date=payload.date,
        time=payload.time,
        status=payload.status,
        notes=payload.notes or "Seguimiento programado",
        points_on_complete=payload.points_on_complete,
        owner_id=payload.owner_id,
        created_by=creator_id,
    )
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def update_followup(db: Session, followup: models.PostConsultFollowUp, payload: schemas.FollowUpUpdate):
    for field, value in payload.dict(exclude_unset=True).items():
        if value is not None:
            setattr(followup, field, value)
    followup.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(followup)
    return followup

