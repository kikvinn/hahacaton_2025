# models.py
from sqlalchemy import String, Integer, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class Event(Base):
    __tablename__ = 'event'
    __table_args__ = (CheckConstraint("sex IN ('M','F')"),)
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey('competition.id', ondelete='CASCADE'), nullable=False)
    exercise_id: Mapped[int] = mapped_column(ForeignKey('exercise.id'), nullable=False)
    sex: Mapped[str | None] = mapped_column(Text)
    age_group_id: Mapped[int | None] = mapped_column(ForeignKey('age_group.id'))
    is_team: Mapped[int] = mapped_column(Integer, default=0)