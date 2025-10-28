from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from core.database import get_db
from auth.service import AuthService
from auth.schemas import UserResponse
from . import schemas, service
from .service import EventService

router = APIRouter()

@router.get("/cards", response_model=List[schemas.EventCardResponse])
def get_event_cards(
    skip: int = Query(0, ge=0),
    limit: int = Query(12, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Получить карточки событий для главной страницы"""
    return EventService.get_events_cards(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[schemas.EventCardResponse])
def search_events(
    query: str = Query(..., min_length=1),
    discipline_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Поиск событий по названию, описанию или местоположению"""
    return EventService.search_events(db, query, discipline_id)

@router.get("/{event_id}", response_model=schemas.EventWithParticipantsResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    """Получить подробную информацию о событии"""
    db_event = EventService.get_event(db, event_id)
    if not db_event or not db_event.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    # Получаем участников
    participants = EventService.get_event_participants(db, event_id)
    
    # Формируем ответ
    event_data = schemas.EventWithParticipantsResponse.from_orm(db_event)
    
    # Добавляем информацию об участниках
    participant_responses = []
    for participant in participants:
        participant_data = schemas.EventParticipantResponse(
            id=participant.id,
            event_id=participant.event_id,
            athlete_id=participant.athlete_id,
            team_id=participant.team_id,
            registration_date=participant.registration_date,
            status=participant.status,
            athlete_name=f"{participant.athlete.last_name} {participant.athlete.first_name}",
            team_name=participant.team.name if participant.team else None
        )
        participant_responses.append(participant_data)
    
    event_data.participants = participant_responses
    return event_data

@router.post("/", response_model=schemas.EventResponse)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(AuthService.get_current_user)
):
    """Создать новое событие (только для организаторов)"""
    # Проверяем, что пользователь является организатором
    if current_user.role not in ['organizer', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organizers can create events"
        )
    
    return EventService.create_event(db, event, current_user.id)

@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(
    event_id: int,
    event_update: schemas.EventUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(AuthService.get_current_user)
):
    """Обновить событие (только организатор события)"""
    db_event = EventService.update_event(db, event_id, event_update, current_user.id)
    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found or you don't have permission to edit it"
        )
    return db_event

@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(AuthService.get_current_user)
):
    """Удалить событие (только организатор события)"""
    success = EventService.delete_event(db, event_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found or you don't have permission to delete it"
        )
    return {"message": "Event deleted successfully"}

@router.get("/my/events", response_model=List[schemas.EventResponse])
def get_my_events(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(AuthService.get_current_user)
):
    """Получить события текущего пользователя (организатора)"""
    if current_user.role not in ['organizer', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organizers can view their events"
        )
    
    return EventService.get_user_events(db, current_user.id)

@router.post("/{event_id}/register", response_model=schemas.EventParticipantResponse)
def register_for_event(
    event_id: int,
    participant: schemas.EventParticipantCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(AuthService.get_current_user)
):
    """Зарегистрироваться на событие"""
    # Проверяем, что пользователь является спортсменом
    if current_user.role not in ['athlete', 'admin']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only athletes can register for events"
        )
    
    # Проверяем, что athlete_id соответствует текущему пользователю
    # (здесь нужна связь между User и Athlete)
    
    db_participant = EventService.register_participant(db, participant, event_id)
    if not db_participant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot register for this event"
        )
    
    # Формируем ответ
    return schemas.EventParticipantResponse(
        id=db_participant.id,
        event_id=db_participant.event_id,
        athlete_id=db_participant.athlete_id,
        team_id=db_participant.team_id,
        registration_date=db_participant.registration_date,
        status=db_participant.status,
        athlete_name=f"{db_participant.athlete.last_name} {db_participant.athlete.first_name}",
        team_name=db_participant.team.name if db_participant.team else None
    )

@router.delete("/{event_id}/unregister")
def unregister_from_event(
    event_id: int,
    athlete_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(AuthService.get_current_user)
):
    """Отменить регистрацию на событие"""
    success = EventService.remove_participant(db, event_id, athlete_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    return {"message": "Successfully unregistered from event"}