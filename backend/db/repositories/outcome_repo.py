from sqlalchemy.orm import Session
from backend.models import Outcome, OutcomeType
from datetime import date
from typing import List, Optional

class OutcomeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_outcome(self, user_id: int, date: date, outcome_type: OutcomeType, **kwargs):
        db_outcome = Outcome(
            user_id=user_id,
            date=date,
            outcome_type=outcome_type,
            **kwargs
        )
        self.db.add(db_outcome)
        self.db.commit()
        self.db.refresh(db_outcome)
        return db_outcome

    def get_user_outcomes(self, user_id: int, limit: int = 100) -> List[Outcome]:
        return self.db.query(Outcome).filter(Outcome.user_id == user_id).order_by(Outcome.date.desc()).limit(limit).all()

    def get_outcome_by_id(self, outcome_id: int) -> Optional[Outcome]:
        return self.db.query(Outcome).filter(Outcome.outcome_id == outcome_id).first()
