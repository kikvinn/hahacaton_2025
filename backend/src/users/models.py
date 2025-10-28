
from sqlalchemy import Column
from backend.src.database.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship, Col

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronymic: Mapped[str | None]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    birth_date = Column()