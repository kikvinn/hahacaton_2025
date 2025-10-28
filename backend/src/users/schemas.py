from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    surname: str
    patronymic: str | None
    # role: str | None


class UserCreate(UserBase):
    email: str
    password: str
    birth_date: date | None
    sex: str | None


class UserPublic(UserBase):
    id: int
