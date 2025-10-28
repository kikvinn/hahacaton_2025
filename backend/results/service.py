from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from . import models, schemas

class ResultService:
    @staticmethod
    def get_result(db: Session, result_id: int) -> Optional[models.Result]:
        return db.query(models.Result).filter(models.Result.id == result_id).first()

    @staticmethod
    def get_results(db: Session, skip: int = 0, limit: int = 100) -> List[models.Result]:
        return db.query(models.Result).offset(skip).limit(limit).all()

    @staticmethod
    def create_result(db: Session, result: schemas.ResultCreate) -> models.Result:
        db_result = models.Result(
            start_entry_id=result.start_entry_id,
            time_ms=result.time_ms,
            distance_mm=result.distance_mm,
            reps=result.reps,
            shooting_points=result.shooting_points,
            series_json=result.series_json,
            dq=result.dq,
            dq_reason=result.dq_reason,
            penalties_json=result.penalties_json,
            points=result.points,
            extra=result.extra
        )
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        return db_result

    @staticmethod
    def update_result(db: Session, result_id: int, result_update: schemas.ResultUpdate) -> Optional[models.Result]:
        db_result = db.query(models.Result).filter(models.Result.id == result_id).first()
        if db_result:
            update_data = result_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_result, field, value)
            db.commit()
            db.refresh(db_result)
        return db_result

    @staticmethod
    def delete_result(db: Session, result_id: int) -> bool:
        db_result = db.query(models.Result).filter(models.Result.id == result_id).first()
        if db_result:
            db.delete(db_result)
            db.commit()
            return True
        return False

    @staticmethod
    def get_start_entry_results(db: Session, start_entry_id: int) -> List[models.Result]:
        return db.query(models.Result).filter(models.Result.start_entry_id == start_entry_id).all()

    @staticmethod
    def get_event_results(db: Session, event_id: int) -> List:
        from events.models import StartEntry
        return db.query(models.Result).join(
            StartEntry,
            models.Result.start_entry_id == StartEntry.id
        ).filter(StartEntry.event_id == event_id).all()

    @staticmethod
    def calculate_points_based_on_exercise_type(result: models.Result) -> int:
        # Здесь можно реализовать бизнес-логику расчета очков
        # на основе типа упражнения и результатов
        if result.time_ms and result.time_ms > 0:
            # Логика для беговых/плавательных дисциплин
            return 1000 - (result.time_ms // 10)
        elif result.distance_mm and result.distance_mm > 0:
            # Логика для метательных дисциплин
            return result.distance_mm // 10
        elif result.reps and result.reps > 0:
            # Логика для силовых упражнений
            return result.reps * 10
        return 0