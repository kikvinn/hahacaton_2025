from pydantic import BaseModel
from typing import Optional

class DisciplineBase(BaseModel):
    exercise_type: str
    exercise: str
    is_team: Optional[bool] = False

class DisciplineCreate(DisciplineBase):
    pass

class DisciplineUpdate(DisciplineBase):
    pass

class DisciplineOut(DisciplineBase):
    id: int

    class Config:
        from_attributes = True