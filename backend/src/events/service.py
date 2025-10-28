from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, func
from typing import List, Optional
from datetime import datetime
from . import models, schemas

class EventService:

    @staticmethod
    def get_event(db: Session, event_id: int) -> Optional[models.Event]:
        return db.get(models.Event, event_id)

    @staticmethod
    def get_events(
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[models.Event]:
        stmt = select(models.Event).offset(skip).limit(limit)
        result = db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    def get_events_cards(
        db: Session,
        skip: int = 0,
        limit: int = 12
    ) -> List[schemas.EventCardResponse]:
        stmt = (
            select(
                models.Event,
                models.User.name.label("organizer_name"),
                models.Discipline.title.label("discipline_name")
            )
            .join(models.User, models.Event.user_id == models.User.id)
            .outerjoin(models.Discipline, models.Event.discipline_id == models.Discipline.id)
            .order_by(models.Event.date)
            .offset(skip)
            .limit(limit)
        )

        result = db.execute(stmt).all()

        return [
            schemas.EventCardResponse(
                id=event.id,
                title=event.title,
                short_description=event.short_description,
                start_date=event.date,
                end_date=event.date,
                location=event.location,
                current_participants=event.current_participants if hasattr(event, 'current_participants') else 0,
                max_participants=event.max_participants if hasattr(event, 'max_participants') else None,
                image_url=event.image_url if hasattr(event, 'image_url') else None,
                organizer_name=organizer_name,
                discipline_name=discipline_name
            )
            for event, organizer_name, discipline_name in result
        ]

    @staticmethod
    def get_user_events(db: Session, user_id: int) -> List[models.Event]:
        stmt = select(models.Event).where(models.Event.user_id == user_id)
        result = db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    def create_event(db: Session, event: schemas.EventCreate, user_id: int) -> models.Event:
        db_event = models.Event(
            user_id=user_id,
            discipline_id=event.discipline_id,
            date=event.date
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def update_event(db: Session, event_id: int, event_update: schemas.EventUpdate, user_id: int) -> Optional[models.Event]:
        stmt = select(models.Event).where(
            models.Event.id == event_id,
            models.Event.user_id == user_id
        )
        result = db.execute(stmt).scalars().first()

        if result:
            update_data = event_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(result, field, value)
            db.commit()
            db.refresh(result)
        return result

    @staticmethod
    def delete_event(db: Session, event_id: int, user_id: int) -> bool:
        stmt = select(models.Event).where(
            models.Event.id == event_id,
            models.Event.user_id == user_id
        )
        result = db.execute(stmt).scalars().first()

        if result:
            db.delete(result)
            db.commit()
            return True
        return False

    @staticmethod
    def search_events(db: Session, query: str, discipline_id: Optional[int] = None) -> List[schemas.EventCardResponse]:
        stmt = (
            select(
                models.Event,
                models.User.name.label("organizer_name"),
                models.Discipline.title.label("discipline_name")
            )
            .join(models.User, models.Event.user_id == models.User.id)
            .outerjoin(models.Discipline, models.Event.discipline_id == models.Discipline.id)
            .filter(
                or_(
                    models.Event.title.ilike(f"%{query}%") if hasattr(models.Event, 'title') else False,
                    models.Event.description.ilike(f"%{query}%") if hasattr(models.Event, 'description') else False,
                    models.Event.location.ilike(f"%{query}%") if hasattr(models.Event, 'location') else False
                )
            )
        )

        if discipline_id:
            stmt = stmt.filter(models.Event.discipline_id == discipline_id)

        result = db.execute(stmt).all()

        return [
            schemas.EventCardResponse(
                id=event.id,
                title=event.title,
                short_description=event.short_description,
                start_date=event.date,
                end_date=event.date,
                location=event.location,
                current_participants=event.current_participants if hasattr(event, 'current_participants') else 0,
                max_participants=event.max_participants if hasattr(event, 'max_participants') else None,
                image_url=event.image_url if hasattr(event, 'image_url') else None,
                organizer_name=organizer_name,
                discipline_name=discipline_name
            )
            for event, organizer_name, discipline_name in result
        ]