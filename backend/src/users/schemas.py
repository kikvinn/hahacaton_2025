from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str | None


class UserCreate(UserBase):
    email: str
    password: str
    birth_date: date | None
    sex: str | None
    role: str | None
