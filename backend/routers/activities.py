from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.db.repositories.activity_log_repo import ActivityLogRepository
from backend.db.repositories.activity_types_repo import ActivityTypesRepository
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

router = APIRouter()

class ActivityLogCreate(BaseModel):
    user_id: int
    activity_name: str
    date: date
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    planned: Optional[bool] = False
    completed: Optional[bool] = False
    postponed: Optional[bool] = False
    energy_level: Optional[int] = None
    notes: Optional[str] = None

@router.post("/log")
async def log_activity(log_data: ActivityLogCreate, db: Session = Depends(get_db_session)):
    types_repo = ActivityTypesRepository(db)
    log_repo = ActivityLogRepository(db)
    
    # Check if activity type exists
    activity_type = types_repo.get_activity_type_by_name(log_data.activity_name)
    if not activity_type:
        raise HTTPException(status_code=400, detail=f"Activity type '{log_data.activity_name}' not found. Please create it first.")
    
    log = log_repo.create_log(
        user_id=log_data.user_id,
        activity_id=activity_type.activity_id,
        date=log_data.date,
        start_time=log_data.start_time,
        end_time=log_data.end_time,
        duration_minutes=log_data.duration_minutes,
        planned=log_data.planned,
        completed=log_data.completed,
        postponed=log_data.postponed,
        energy_level=log_data.energy_level,
        notes=log_data.notes
    )
    return log

@router.get("/logs/{user_id}")
async def get_logs(user_id: int, db: Session = Depends(get_db_session)):
    log_repo = ActivityLogRepository(db)
    return log_repo.get_user_logs(user_id)
