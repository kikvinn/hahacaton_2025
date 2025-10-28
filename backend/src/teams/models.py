from backend.src.database.init_db import Base
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Teams(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), nullable=False)
