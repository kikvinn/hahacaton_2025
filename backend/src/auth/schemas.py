from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
