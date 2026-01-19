from sqlalchemy.orm import Session
from backend.models import AnalyticsSummary
from datetime import datetime
from typing import List, Optional

class AnalyticsSummaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_summary(self, user_id: int, period_type: str, period_start: datetime, period_end: datetime, **kwargs):
        db_summary = AnalyticsSummary(
            user_id=user_id,
            period_type=period_type,
            period_start=period_start,
            period_end=period_end,
            **kwargs
        )
        self.db.add(db_summary)
        self.db.commit()
        self.db.refresh(db_summary)
        return db_summary

    def get_latest_summaries(self, user_id: int, limit: int = 5) -> List[AnalyticsSummary]:
        return self.db.query(AnalyticsSummary).filter(
            AnalyticsSummary.user_id == user_id
        ).order_by(AnalyticsSummary.generated_at.desc()).limit(limit).all()
