from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

class EventService:
    @staticmethod
    def get_event(db: Session, event_id: int) -> Optional[models.Event]:
        return db.query(models.Event).filter(models.Event.id == event_id).first()

    @staticmethod
    def get_events(db: Session, skip: int = 0, limit: int = 100) -> List[models.Event]:
        return db.query(models.Event).offset(skip).limit(limit).all()

    @staticmethod
    def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
        db_event = models.Event(
            competition_id=event.competition_id,
            exercise_id=event.exercise_id,
            sex=event.sex,
            age_group_id=event.age_group_id,
            is_team=event.is_team,
            discipline_id=event.discipline_id,
            bundle_id=event.bundle_id,
            start_datetime=event.start_datetime,
            extra=event.extra
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def update_event(db: Session, event_id: int, event_update: schemas.EventUpdate) -> Optional[models.Event]:
        db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if db_event:
            update_data = event_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_event, field, value)
            db.commit()
            db.refresh(db_event)
        return db_event

    @staticmethod
    def delete_event(db: Session, event_id: int) -> bool:
        db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if db_event:
            db.delete(db_event)
            db.commit()
            return True
        return False

    @staticmethod
    def get_competition_events(db: Session, competition_id: int) -> List[models.Event]:
        return db.query(models.Event).filter(models.Event.competition_id == competition_id).all()

    @staticmethod
    def create_heat(db: Session, heat: schemas.HeatCreate) -> models.Heat:
        db_heat = models.Heat(
            event_id=heat.event_id,
            seq=heat.seq,
            starts_at=heat.starts_at,
            extra=heat.extra
        )
        db.add(db_heat)
        db.commit()
        db.refresh(db_heat)
        return db_heat

    @staticmethod
    def get_event_heats(db: Session, event_id: int) -> List[models.Heat]:
        return db.query(models.Heat).filter(models.Heat.event_id == event_id).order_by(models.Heat.seq).all()

    @staticmethod
    def create_start_entry(db: Session, start_entry: schemas.StartEntryCreate) -> models.StartEntry:
        db_start_entry = models.StartEntry(
            event_id=start_entry.event_id,
            heat_id=start_entry.heat_id,
            lane=start_entry.lane,
            athlete_id=start_entry.athlete_id,
            team_id=start_entry.team_id,
            bib_number=start_entry.bib_number,
            order_in_heat=start_entry.order_in_heat
        )
        db.add(db_start_entry)
        db.commit()
        db.refresh(db_start_entry)
        return db_start_entry

    @staticmethod
    def get_event_start_entries(db: Session, event_id: int) -> List[models.StartEntry]:
        return db.query(models.StartEntry).filter(models.StartEntry.event_id == event_id).all()