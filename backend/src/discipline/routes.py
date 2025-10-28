from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from disciplines import schemas, crud
from backend.src.database.session import get_db

router = APIRouter(prefix="/disciplines", tags=["Disciplines"])

@router.post("/", response_model=schemas.DisciplineOut)
def create_discipline(discipline: schemas.DisciplineCreate, db: Session = Depends(get_db)):
    return crud.create_discipline(db, discipline)

@router.get("/{discipline_id}", response_model=schemas.DisciplineOut)
def read_discipline(discipline_id: int, db: Session = Depends(get_db)):
    db_discipline = crud.get_discipline(db, discipline_id)
    if not db_discipline:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return db_discipline

@router.get("/", response_model=list[schemas.DisciplineOut])
def read_disciplines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_disciplines(db, skip=skip, limit=limit)

@router.put("/{discipline_id}", response_model=schemas.DisciplineOut)
def update_discipline(discipline_id: int, discipline: schemas.DisciplineUpdate, db: Session = Depends(get_db)):
    db_discipline = crud.update_discipline(db, discipline_id, discipline)
    if not db_discipline:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return db_discipline

@router.delete("/{discipline_id}")
def delete_discipline(discipline_id: int, db: Session = Depends(get_db)):
    db_discipline = crud.delete_discipline(db, discipline_id)
    if not db_discipline:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return {"detail": "Discipline deleted"}