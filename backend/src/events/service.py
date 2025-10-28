from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime
from . import models, schemas

class EventService:
    @staticmethod
    def get_event(db: Session, event_id: int) -> Optional[models.Event]:
        return db.query(models.Event).filter(models.Event.id == event_id).first()

    @staticmethod
    def get_events(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        is_active: bool = True,
        is_public: bool = True
    ) -> List[models.Event]:
        query = db.query(models.Event)
        
        if is_active:
            query = query.filter(models.Event.is_active == True)
        if is_public:
            query = query.filter(models.Event.is_public == True)
            
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_events_cards(
        db: Session,
        skip: int = 0,
        limit: int = 12
    ) -> List[schemas.EventCardResponse]:
        from auth.models import User
        from references.models import Discipline
        
        events = db.query(
            models.Event,
            User.full_name,
            Discipline.name
        ).join(
            User, models.Event.organizer_id == User.id
        ).outerjoin(
            Discipline, models.Event.discipline_id == Discipline.id
        ).filter(
            models.Event.is_active == True,
            models.Event.is_public == True,
            models.Event.start_date >= datetime.utcnow()
        ).order_by(
            models.Event.start_date
        ).offset(skip).limit(limit).all()
        
        return [
            schemas.EventCardResponse(
                id=event.id,
                title=event.title,
                short_description=event.short_description,
                start_date=event.start_date,
                end_date=event.end_date,
                location=event.location,
                current_participants=event.current_participants,
                max_participants=event.max_participants,
                image_url=event.image_url,
                organizer_name=full_name,
                discipline_name=discipline_name
            )
            for event, full_name, discipline_name in events
        ]

    @staticmethod
    def get_user_events(db: Session, user_id: int) -> List[models.Event]:
        return db.query(models.Event).filter(
            models.Event.organizer_id == user_id
        ).order_by(models.Event.created_at.desc()).all()

    @staticmethod
    def create_event(db: Session, event: schemas.EventCreate, organizer_id: int) -> models.Event:
        db_event = models.Event(
            title=event.title,
            description=event.description,
            short_description=event.short_description,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            max_participants=event.max_participants,
            is_public=event.is_public,
            image_url=event.image_url,
            organizer_id=organizer_id,
            discipline_id=event.discipline_id
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def update_event(db: Session, event_id: int, event_update: schemas.EventUpdate, user_id: int) -> Optional[models.Event]:
        db_event = db.query(models.Event).filter(
            models.Event.id == event_id,
            models.Event.organizer_id == user_id
        ).first()
        
        if db_event:
            update_data = event_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_event, field, value)
            db_event.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_event)
        return db_event

    @staticmethod
    def delete_event(db: Session, event_id: int, user_id: int) -> bool:
        db_event = db.query(models.Event).filter(
            models.Event.id == event_id,
            models.Event.organizer_id == user_id
        ).first()
        
        if db_event:
            # Вместо удаления деактивируем событие
            db_event.is_active = False
            db.commit()
            return True
        return False

    @staticmethod
    def register_participant(db: Session, participant: schemas.EventParticipantCreate, event_id: int) -> Optional[models.EventParticipant]:
        # Проверяем существование события
        event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if not event or not event.is_active:
            return None
        
        # Проверяем наличие мест
        if event.max_participants and event.current_participants >= event.max_participants:
            return None
        
        # Проверяем, не зарегистрирован ли уже участник
        existing_participant = db.query(models.EventParticipant).filter(
            models.EventParticipant.event_id == event_id,
            models.EventParticipant.athlete_id == participant.athlete_id
        ).first()
        
        if existing_participant:
            return None
        
        db_participant = models.EventParticipant(
            event_id=event_id,
            athlete_id=participant.athlete_id,
            team_id=participant.team_id
        )
        
        db.add(db_participant)
        
        # Обновляем счетчик участников
        event.current_participants += 1
        db.commit()
        db.refresh(db_participant)
        return db_participant

    @staticmethod
    def get_event_participants(db: Session, event_id: int) -> List[models.EventParticipant]:
        return db.query(models.EventParticipant).filter(
            models.EventParticipant.event_id == event_id
        ).all()

    @staticmethod
    def remove_participant(db: Session, event_id: int, athlete_id: int) -> bool:
        db_participant = db.query(models.EventParticipant).filter(
            models.EventParticipant.event_id == event_id,
            models.EventParticipant.athlete_id == athlete_id
        ).first()
        
        if db_participant:
            event = db.query(models.Event).filter(models.Event.id == event_id).first()
            if event:
                event.current_participants -= 1
            db.delete(db_participant)
            db.commit()
            return True
        return False

    @staticmethod
    def search_events(db: Session, query: str, discipline_id: Optional[int] = None) -> List[schemas.EventCardResponse]:
        from auth.models import User
        from references.models import Discipline
        
        search_query = db.query(
            models.Event,
            User.full_name,
            Discipline.name
        ).join(
            User, models.Event.organizer_id == User.id
        ).outerjoin(
            Discipline, models.Event.discipline_id == Discipline.id
        ).filter(
            models.Event.is_active == True,
            models.Event.is_public == True,
            or_(
                models.Event.title.ilike(f"%{query}%"),
                models.Event.description.ilike(f"%{query}%"),
                models.Event.location.ilike(f"%{query}%")
            )
        )
        
        if discipline_id:
            search_query = search_query.filter(models.Event.discipline_id == discipline_id)
            
        results = search_query.order_by(models.Event.start_date).all()
        
        return [
            schemas.EventCardResponse(
                id=event.id,
                title=event.title,
                short_description=event.short_description,
                start_date=event.start_date,
                end_date=event.end_date,
                location=event.location,
                current_participants=event.current_participants,
                max_participants=event.max_participants,
                image_url=event.image_url,
                organizer_name=full_name,
                discipline_name=discipline_name
            )
            for event, full_name, discipline_name in results
        ]