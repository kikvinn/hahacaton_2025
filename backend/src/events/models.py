from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from core.database import Base

class Event(Base):
    __tablename__ = 'events'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    short_description: Mapped[str] = mapped_column(String(300))
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(200))
    max_participants: Mapped[Optional[int]] = mapped_column(Integer)
    current_participants: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связь с организатором
    organizer_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    organizer: Mapped['User'] = relationship('User', back_populates='organized_events')
    
    # Связь с дисциплиной
    discipline_id: Mapped[Optional[int]] = mapped_column(ForeignKey('discipline.id'))
    discipline: Mapped[Optional['Discipline']] = relationship()
    
    # Связь с участниками
    participants: Mapped[list['EventParticipant']] = relationship(
        'EventParticipant', 
        back_populates='event',
        cascade='all, delete-orphan'
    )

class EventParticipant(Base):
    __tablename__ = 'event_participants'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey('events.id'), nullable=False)
    athlete_id: Mapped[int] = mapped_column(ForeignKey('athlete.id'), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(20), default='registered')  # registered, approved, cancelled
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey('team.id'))
    
    event: Mapped['Event'] = relationship('Event', back_populates='participants')
    athlete: Mapped['Athlete'] = relationship('Athlete')
    team: Mapped[Optional['Team']] = relationship()