import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

session_logger = logging.getLogger("database.session")


engine = create_engine("sqlite:///../database.db")

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

Base = declarative_base()


def get_session() -> Session:
    try:
        with SessionLocal() as session:
            yield session
        session_logger.debug("Сессия базы данных успешно создана и проверена")

    except SQLAlchemyError as e:
        session_logger.error(f"Ошибка SQLAlchemy при работе с сессией: {e!s}")
        raise
    except Exception as e:
        session_logger.error(f"Неожиданная ошибка при работе с сессией: {e!s}")
        raise


SessionDep = Annotated[Session, Depends(get_session)]
