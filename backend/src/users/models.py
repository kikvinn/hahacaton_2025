from datetime import date
from typing import Literal

from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.session import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    birth_date: Mapped[date | None] = mapped_column(Date)
    sex: Mapped[str | None]

    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"))
    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"))
