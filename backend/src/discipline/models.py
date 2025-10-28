from sqlalchemy import Column
from backend.src.database.session import Base
from sqlalchemy.orm import Mapped, mapped_column

class Discipline(Base):
    __tablename__ = "disciplines"

    id: Mapped[int] = mapped_column(primary_key=True)
    exercise_type: Mapped[str]  
    exercise: Mapped[str]       
    is_team: Mapped[bool] = mapped_column(default=False)
    events: Mapped[List["Event"]] = relationship("Event", back_populates="discipline")