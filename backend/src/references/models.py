# models.py
from sqlalchemy import String, Integer, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class AgeGroup(Base):
    __tablename__ = 'age_group'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    min_years: Mapped[int] = mapped_column(Integer, nullable=False)
    max_years: Mapped[int] = mapped_column(Integer, nullable=False)
    veteran: Mapped[int] = mapped_column(Integer, default=0)

class Exercise(Base):
    __tablename__ = 'exercise'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    kind: Mapped[str] = mapped_column(Text, nullable=False)
    params: Mapped[str] = mapped_column(Text, default='{}')