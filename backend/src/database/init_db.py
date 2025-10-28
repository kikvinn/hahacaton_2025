import logging

from sqlalchemy.orm import Session

from src.roles.models import Roles
from src.teams.models import Team
from src.users.models import User

from .session import Base, engine

db_logger = logging.getLogger("database")


def create_db() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        db_logger.error(f"Ошибка при создании базы данных: {e!s}")
        raise


def drop_db() -> None:
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception as e:
        db_logger.error(f"Ошибка при удалении базы данных: {e!s}")
        raise
