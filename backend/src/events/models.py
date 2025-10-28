from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class Event(Base):
    __tablename__ = 'events'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    discipline_id: Mapped[int] = mapped_column(ForeignKey('disciplines.id'))  # disciplines, а не discipline?
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Связь
    user: Mapped["User"] = relationship("User", back_populates="events")
    discipline: Mapped["Discipline"] = relationship("Discipline", back_populates="events")