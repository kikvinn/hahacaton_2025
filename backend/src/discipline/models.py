from sqlalchemy import Column
from sqlalchemy.orm import Mapped, mapped_column

from src.database.session import Base


class Discipline(Base):
    __tablename__ = "disciplines"

    id: Mapped[int] = mapped_column(primary_key=True)
    exercise_type: Mapped[str]
    exercise: Mapped[str]
    is_team: Mapped[bool] = mapped_column(default=False)
