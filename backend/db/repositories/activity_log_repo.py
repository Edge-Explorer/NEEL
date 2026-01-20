from sqlalchemy.orm import Session
from backend.models import ActivityLog
from datetime import datetime
from typing import List, Optional

class ActivityLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_log(self, user_id: int, activity_id: int, date: datetime.date, **kwargs):
        db_log = ActivityLog(
            user_id=user_id,
            activity_id=activity_id,
            date=date,
            **kwargs
        )
        self.db.add(db_log)
        self.db.commit()
        self.db.refresh(db_log)
        return db_log

    def get_user_logs(self, user_id: int, limit: int = 100) -> List[ActivityLog]:
        return self.db.query(ActivityLog).filter(ActivityLog.user_id == user_id).order_by(ActivityLog.created_at.desc()).limit(limit).all()

    def get_log_by_id(self, log_id: int) -> Optional[ActivityLog]:
        return self.db.query(ActivityLog).filter(ActivityLog.log_id == log_id).first()

    def update_log(self, log_id: int, **kwargs) -> Optional[ActivityLog]:
        db_log = self.get_log_by_id(log_id)
        if db_log:
            for key, value in kwargs.items():
                setattr(db_log, key, value)
            self.db.commit()
            self.db.refresh(db_log)
        return db_log

    def delete_log(self, log_id: int) -> bool:
        db_log = self.get_log_by_id(log_id)
        if db_log:
            self.db.delete(db_log)
            self.db.commit()
            return True
        return False
