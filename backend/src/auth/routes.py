from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from src.database.session import SessionDep
from src.users.schemas import UserCreate, UserPublic

from .schemas import Token, UserLogin
from .service import AuthService

auth = APIRouter()
security = HTTPBearer()


@auth.post("/register", response_model=UserPublic)
def register(user_data: UserCreate, db: SessionDep):
    # Check if user already exists
    db_user = AuthService.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    user = AuthService.create_user(db=db, user=user_data)
    return user


@auth.post("/login", response_model=Token)
def login(response: Response, user_data: UserLogin, db: SessionDep):
    # Authenticate user
    user = AuthService.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
        )

    # Create tokens
    access_token = AuthService.create_access_token(data={"sub": user.email, "user_id": user.id})
    refresh_token = AuthService.create_refresh_token(data={"sub": user.email, "user_id": user.id})

    # Set cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=30 * 60,  # 30 minutes
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 30 * 60,  # 30 minutes in seconds
    }


@auth.post("/logout")
def logout(response: Response):
    # Clear cookies
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Successfully logged out"}


@auth.post("/refresh", response_model=Token)
def refresh_token(response: Response, db: SessionDep):
    # In a real implementation, you'd get the refresh token from cookies
    # and verify it before issuing a new access token
    # This is a simplified version
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Refresh endpoint not implemented"
    )


@auth.get("/me", response_model=UserPublic)
def get_current_user(db: SessionDep, token: str = Depends(security)):
    user = AuthService.get_current_user(db, token.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials"
        )
    return user
