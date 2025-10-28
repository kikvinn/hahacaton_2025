from pydantic import BaseModel


class TeamCreate(BaseModel):
    name: str
    users: list[int]


class TeamPublic(BaseModel):
    id: int
    name: str
    users: list[int]
