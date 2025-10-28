from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.database.session import SessionDep

from .schemas import TeamCreate, TeamPublic
from .service import create

teams = APIRouter()


@teams.post("/", status_code=status.HTTP_201_CREATED, response_model=TeamPublic)
def create_user(
    db: SessionDep,
    team_in: TeamCreate,
):
    try:
        user = create(db, user_in=team_in)

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
