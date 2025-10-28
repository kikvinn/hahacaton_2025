from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.database.session import SessionDep

from .schemas import UserCreate, UserPublic
from .service import create, get, get_multi

users = APIRouter()


@users.get("/", response_model=list[UserPublic])
def get_all(
    db: SessionDep,
    skip: int = 0,
    limit: int = 50,
):
    try:
        users_list = get_multi(db, skip, limit)
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {e}",
        ) from e
    else:
        return users_list


@users.get("/{user_id}", response_model=UserPublic)
def get_user(
    db: SessionDep,
    user_id: int,
):
    try:
        user = get(db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error {e}",
        )
    else:
        return user


@users.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(
    db: SessionDep,
    user_in: UserCreate,
):
    try:
        user = create(db, user_in=user_in)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    else:
        return user
