from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.db.repositories.activity_log_repo import ActivityLogRepository
from backend.db.repositories.activity_types_repo import ActivityTypesRepository
from backend.utils.auth import get_current_user
from backend.models import User
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

router = APIRouter()

class ActivityLogCreate(BaseModel):
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

class ActivityLogUpdate(BaseModel):
    activity_name: Optional[str] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None
    energy_level: Optional[int] = None

@router.post("/log")
async def log_activity(
    log_data: ActivityLogCreate, 
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    types_repo = ActivityTypesRepository(db)
    log_repo = ActivityLogRepository(db)
    
    # Check if activity type exists
    activity_type = types_repo.get_activity_type_by_name(log_data.activity_name)
    if not activity_type:
        # If it's a new activity, we'll auto-create it under 'Work' or 'Personal' for now
        # or just return error as before. Let's stick to error for control.
        raise HTTPException(status_code=400, detail=f"Activity type '{log_data.activity_name}' not found.")
    
    log = log_repo.create_log(
        user_id=current_user.user_id,
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

@router.put("/log/{log_id}")
async def update_activity_log(
    log_id: int,
    update_data: ActivityLogUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    log_repo = ActivityLogRepository(db)
    log = log_repo.get_log_by_id(log_id)
    
    if not log or log.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Log not found.")
        
    # Check 24h limit
    if (datetime.utcnow() - log.created_at).total_seconds() > 86400:
        raise HTTPException(status_code=403, detail="Logs can only be edited within 24 hours.")
        
    update_dict = {}
    if update_data.activity_name:
        types_repo = ActivityTypesRepository(db)
        act_type = types_repo.get_activity_type_by_name(update_data.activity_name)
        if act_type:
            update_dict["activity_id"] = act_type.activity_id
            
    if update_data.duration_minutes is not None:
        update_dict["duration_minutes"] = update_data.duration_minutes
    if update_data.notes is not None:
        update_dict["notes"] = update_data.notes
    if update_data.energy_level is not None:
        update_dict["energy_level"] = update_data.energy_level
        
    updated_log = log_repo.update_log(log_id, **update_dict)
    return updated_log

@router.delete("/log/{log_id}")
async def delete_activity_log(
    log_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    log_repo = ActivityLogRepository(db)
    log = log_repo.get_log_by_id(log_id)
    
    if not log or log.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Log not found.")
        
    # Check 24h limit
    if (datetime.utcnow() - log.created_at).total_seconds() > 86400:
        raise HTTPException(status_code=403, detail="Logs can only be deleted within 24 hours.")
        
    log_repo.delete_log(log_id)
    return {"status": "success"}
