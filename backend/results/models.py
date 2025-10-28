# models.py
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from datetime import datetime

class Result(Base):
    __tablename__ = 'result'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_entry_id: Mapped[int] = mapped_column(ForeignKey('start_entry.id', ondelete='CASCADE'), nullable=False)
    time_ms: Mapped[int | None] = mapped_column(Integer)
    distance_mm: Mapped[int | None] = mapped_column(Integer)
    reps: Mapped[int | None] = mapped_column(Integer)
    shooting_points: Mapped[int | None] = mapped_column(Integer)
    series_json: Mapped[str | None] = mapped_column(Text)
    dq: Mapped[int] = mapped_column(Integer, default=0)
    dq_reason: Mapped[str | None] = mapped_column(Text)
    penalties_json: Mapped[str] = mapped_column(Text, default='[]')
    points: Mapped[int | None] = mapped_column(Integer)
    extra: Mapped[str] = mapped_column(Text, default='{}')
    created_at: Mapped[str] = mapped_column(Text, default=lambda: datetime.now().isoformat())