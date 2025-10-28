from backend.src.database.session import Base
from sqlalchemy.orm import Mapped, mapped_column


class Roles(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
