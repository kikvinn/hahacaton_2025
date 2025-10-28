from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

class ReferenceService:
    # Age Group operations
    @staticmethod
    def get_age_group(db: Session, age_group_id: int) -> Optional[models.AgeGroup]:
        return db.query(models.AgeGroup).filter(models.AgeGroup.id == age_group_id).first()

    @staticmethod
    def get_age_groups(db: Session, skip: int = 0, limit: int = 100) -> List[models.AgeGroup]:
        return db.query(models.AgeGroup).offset(skip).limit(limit).all()

    @staticmethod
    def create_age_group(db: Session, age_group: schemas.AgeGroupCreate) -> models.AgeGroup:
        db_age_group = models.AgeGroup(
            code=age_group.code,
            min_years=age_group.min_years,
            max_years=age_group.max_years,
            veteran=age_group.veteran
        )
        db.add(db_age_group)
        db.commit()
        db.refresh(db_age_group)
        return db_age_group

    # Exercise operations
    @staticmethod
    def get_exercise(db: Session, exercise_id: int) -> Optional[models.Exercise]:
        return db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()

    @staticmethod
    def get_exercises(db: Session, skip: int = 0, limit: int = 100) -> List[models.Exercise]:
        return db.query(models.Exercise).offset(skip).limit(limit).all()

    @staticmethod
    def create_exercise(db: Session, exercise: schemas.ExerciseCreate) -> models.Exercise:
        db_exercise = models.Exercise(
            code=exercise.code,
            name=exercise.name,
            kind=exercise.kind,
            params=exercise.params
        )
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)
        return db_exercise

    @staticmethod
    def get_exercises_by_kind(db: Session, kind: str) -> List[models.Exercise]:
        return db.query(models.Exercise).filter(models.Exercise.kind == kind).all()

    # Discipline operations
    @staticmethod
    def get_discipline(db: Session, discipline_id: int) -> Optional[models.Discipline]:
        return db.query(models.Discipline).filter(models.Discipline.id == discipline_id).first()

    @staticmethod
    def get_disciplines(db: Session, skip: int = 0, limit: int = 100) -> List[models.Discipline]:
        return db.query(models.Discipline).offset(skip).limit(limit).all()

    @staticmethod
    def create_discipline(db: Session, discipline: schemas.DisciplineCreate) -> models.Discipline:
        db_discipline = models.Discipline(
            code=discipline.code,
            name=discipline.name
        )
        db.add(db_discipline)
        db.commit()
        db.refresh(db_discipline)
        return db_discipline

    # Discipline Bundle operations
    @staticmethod
    def create_discipline_bundle(db: Session, bundle: schemas.DisciplineBundleCreate) -> models.DisciplineBundle:
        db_bundle = models.DisciplineBundle(
            discipline_id=bundle.discipline_id,
            sex=bundle.sex,
            age_group_id=bundle.age_group_id
        )
        db.add(db_bundle)
        db.commit()
        db.refresh(db_bundle)
        return db_bundle

    @staticmethod
    def add_bundle_item(db: Session, item: schemas.DisciplineBundleItemCreate) -> models.DisciplineBundleItem:
        db_item = models.DisciplineBundleItem(
            bundle_id=item.bundle_id,
            seq=item.seq,
            exercise_id=item.exercise_id
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def get_bundle_items(db: Session, bundle_id: int) -> List[models.DisciplineBundleItem]:
        return db.query(models.DisciplineBundleItem).filter(
            models.DisciplineBundleItem.bundle_id == bundle_id
        ).order_by(models.DisciplineBundleItem.seq).all()