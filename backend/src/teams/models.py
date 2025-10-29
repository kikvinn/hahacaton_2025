from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.session import Base


class Team(Base):
    __tablename__ = "teams"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    users: Mapped[list["User"]] = relationship(back_populates="team")
    # event_id: Mapped[int] = mapped_column(ForeignKey("event.id"), nullable=False)
