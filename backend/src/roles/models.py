from sqlalchemy.orm import Mapped, mapped_column

from src.database.session import Base


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
