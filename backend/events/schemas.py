from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class EventBase(BaseModel):
    title: str
    description: str
    short_description: str
    start_date: datetime
    end_date: datetime
    location: str
    max_participants: Optional[int] = None
    is_public: bool = True
    image_url: Optional[str] = None
    discipline_id: Optional[int] = None

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None
    is_public: Optional[bool] = None
    image_url: Optional[str] = None
    discipline_id: Optional[int] = None

class EventResponse(EventBase):
    id: int
    organizer_id: int
    current_participants: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    organizer_name: Optional[str] = None
    discipline_name: Optional[str] = None

    class Config:
        from_attributes = True

class EventCardResponse(BaseModel):
    id: int
    title: str
    short_description: str
    start_date: datetime
    end_date: datetime
    location: str
    current_participants: int
    max_participants: Optional[int]
    image_url: Optional[str]
    organizer_name: str
    discipline_name: Optional[str]

    class Config:
        from_attributes = True

class EventParticipantBase(BaseModel):
    athlete_id: int
    team_id: Optional[int] = None

class EventParticipantCreate(EventParticipantBase):
    pass

class EventParticipantResponse(EventParticipantBase):
    id: int
    event_id: int
    registration_date: datetime
    status: str
    athlete_name: str
    team_name: Optional[str]

    class Config:
        from_attributes = True

class EventWithParticipantsResponse(EventResponse):
    participants: List[EventParticipantResponse] = []