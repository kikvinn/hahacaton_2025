from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    surname: str
    patronymic: str | None = None
    # role: str | None


class UserCreate(UserBase):
    email: str
    password: str
    birth_date: date | None = None
    sex: str | None = None


class UserPublic(UserBase):
    id: int
