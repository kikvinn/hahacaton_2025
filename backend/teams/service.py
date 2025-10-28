from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from . import models, schemas

class TeamService:
    @staticmethod
    def get_team(db: Session, team_id: int) -> Optional[models.Team]:
        return db.query(models.Team).filter(models.Team.id == team_id).first()

    @staticmethod
    def get_teams(db: Session, skip: int = 0, limit: int = 100) -> List[models.Team]:
        return db.query(models.Team).offset(skip).limit(limit).all()

    @staticmethod
    def create_team(db: Session, team: schemas.TeamCreate) -> models.Team:
        db_team = models.Team(
            competition_id=team.competition_id,
            name=team.name,
            club=team.club,
            is_mixed=team.is_mixed
        )
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return db_team

    @staticmethod
    def update_team(db: Session, team_id: int, team_update: schemas.TeamUpdate) -> Optional[models.Team]:
        db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
        if db_team:
            update_data = team_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_team, field, value)
            db.commit()
            db.refresh(db_team)
        return db_team

    @staticmethod
    def delete_team(db: Session, team_id: int) -> bool:
        db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
        if db_team:
            db.delete(db_team)
            db.commit()
            return True
        return False

    @staticmethod
    def get_competition_teams(db: Session, competition_id: int) -> List[models.Team]:
        return db.query(models.Team).filter(models.Team.competition_id == competition_id).all()

    @staticmethod
    def add_team_member(db: Session, team_member: schemas.TeamMemberCreate) -> models.TeamMember:
        db_team_member = models.TeamMember(
            team_id=team_member.team_id,
            athlete_id=team_member.athlete_id,
            role=team_member.role
        )
        db.add(db_team_member)
        db.commit()
        db.refresh(db_team_member)
        return db_team_member

    @staticmethod
    def remove_team_member(db: Session, team_id: int, athlete_id: int) -> bool:
        db_team_member = db.query(models.TeamMember).filter(
            models.TeamMember.team_id == team_id,
            models.TeamMember.athlete_id == athlete_id
        ).first()
        if db_team_member:
            db.delete(db_team_member)
            db.commit()
            return True
        return False

    @staticmethod
    def get_team_members(db: Session, team_id: int) -> List:
        from athletes.models import Athlete
        return db.query(Athlete).join(
            models.TeamMember, 
            Athlete.id == models.TeamMember.athlete_id
        ).filter(models.TeamMember.team_id == team_id).all()