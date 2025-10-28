# models.py
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class Team(Base):
    __tablename__ = 'team'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    competition_id: Mapped[int] = mapped_column(ForeignKey('competition.id', ondelete='CASCADE'), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    club: Mapped[str | None] = mapped_column(Text)
    is_mixed: Mapped[int] = mapped_column(Integer, default=0)