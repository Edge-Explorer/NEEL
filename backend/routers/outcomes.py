from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.db.repositories.outcome_repo import OutcomeRepository
from backend.models import OutcomeType
from pydantic import BaseModel
from datetime import date
from typing import List, Optional

router = APIRouter()

class OutcomeCreate(BaseModel):
    user_id: int
    date: date
    outcome_type: OutcomeType
    outcome_value: str
    related_activity_id: Optional[int] = None

@router.post("/")
async def create_outcome(outcome_data: OutcomeCreate, db: Session = Depends(get_db_session)):
    repo = OutcomeRepository(db)
    return repo.create_outcome(
        user_id=outcome_data.user_id,
        date=outcome_data.date,
        outcome_type=outcome_data.outcome_type,
        outcome_value=outcome_data.outcome_value,
        related_activity_id=outcome_data.related_activity_id
    )

@router.get("/{user_id}")
async def get_outcomes(user_id: int, db: Session = Depends(get_db_session)):
    repo = OutcomeRepository(db)
    return repo.get_user_outcomes(user_id)
