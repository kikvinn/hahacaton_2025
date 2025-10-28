from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.auth.service import AuthService

from .models import User
from .schemas import UserCreate, UserUpdate


def get(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_multi(db: Session, skip: int = 0, limit: int = 50) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def delete(db: Session, user_id: int) -> User | None:
    try:
        user = get(db, user_id)
        if user is None:
            return None

        db.delete(user)
        db.commit()

        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e
