from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime
from . import models, schemas

class CompetitionService:
    @staticmethod
    def get_competition(db: Session, competition_id: int) -> Optional[models.Competition]:
        return db.query(models.Competition).filter(models.Competition.id == competition_id).first()

    @staticmethod
    def get_competitions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Competition]:
        return db.query(models.Competition).offset(skip).limit(limit).all()

    @staticmethod
    def create_competition(db: Session, competition: schemas.CompetitionCreate) -> models.Competition:
        db_competition = models.Competition(
            name=competition.name,
            level=competition.level,
            city=competition.city,
            country=competition.country,
            venue=competition.venue,
            start_date=competition.start_date,
            end_date=competition.end_date
        )
        db.add(db_competition)
        db.commit()
        db.refresh(db_competition)
        return db_competition

    @staticmethod
    def update_competition(db: Session, competition_id: int, competition_update: schemas.CompetitionUpdate) -> Optional[models.Competition]:
        db_competition = db.query(models.Competition).filter(models.Competition.id == competition_id).first()
        if db_competition:
            update_data = competition_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_competition, field, value)
            db.commit()
            db.refresh(db_competition)
        return db_competition

    @staticmethod
    def delete_competition(db: Session, competition_id: int) -> bool:
        db_competition = db.query(models.Competition).filter(models.Competition.id == competition_id).first()
        if db_competition:
            db.delete(db_competition)
            db.commit()
            return True
        return False

    @staticmethod
    def search_competitions(db: Session, query: str) -> List[models.Competition]:
        return db.query(models.Competition).filter(
            or_(
                models.Competition.name.ilike(f"%{query}%"),
                models.Competition.city.ilike(f"%{query}%"),
                models.Competition.country.ilike(f"%{query}%"),
                models.Competition.venue.ilike(f"%{query}%")
            )
        ).all()

    @staticmethod
    def get_upcoming_competitions(db: Session) -> List[models.Competition]:
        today = datetime.now().date().isoformat()
        return db.query(models.Competition).filter(
            models.Competition.start_date >= today
        ).order_by(models.Competition.start_date).all()

    @staticmethod
    def get_competition_teams(db: Session, competition_id: int) -> List:
        from teams.models import Team
        return db.query(Team).filter(Team.competition_id == competition_id).all()