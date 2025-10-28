from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .models import User
from .schemas import UserCreate


def get(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_multi(db: Session, skip: int = 0, limit: int = 50) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()
def create(db:Session, user_in: UserCreate) ->User:
    