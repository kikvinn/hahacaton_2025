from sqlalchemy.orm import Session
from disciplines.models import Discipline
from disciplines.schemas import DisciplineCreate, DisciplineUpdate

def get_discipline(db: Session, discipline_id: int):
    return db.query(Discipline).filter(Discipline.id == discipline_id).first()

def get_disciplines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Discipline).offset(skip).limit(limit).all()

def create_discipline(db: Session, discipline: DisciplineCreate):
    db_discipline = Discipline(**discipline.dict())
    db.add(db_discipline)
    db.commit()
    db.refresh(db_discipline)
    return db_discipline

def update_discipline(db: Session, discipline_id: int, discipline: DisciplineUpdate):
    db_discipline = db.query(Discipline).filter(Discipline.id == discipline_id).first()
    if not db_discipline:
        return None
    for key, value in discipline.dict().items():
        setattr(db_discipline, key, value)
    db.commit()
    db.refresh(db_discipline)
    return db_discipline

def delete_discipline(db: Session, discipline_id: int):
    db_discipline = db.query(Discipline).filter(Discipline.id == discipline_id).first()
    if db_discipline:
        db.delete(db_discipline)
        db.commit()
    return db_discipline