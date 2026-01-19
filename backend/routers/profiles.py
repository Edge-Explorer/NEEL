from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.db.repositories.user_profile_repo import UserProfileRepository
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter()

class UserProfileUpdate(BaseModel):
    primary_goal: str
    secondary_goals: Optional[List[str]] = None
    focus_areas: Optional[List[str]] = None
    priority_order: Optional[List[str]] = None
    time_horizon: Optional[str] = None

@router.post("/{user_id}")
async def update_profile(user_id: int, profile_data: UserProfileUpdate, db: Session = Depends(get_db_session)):
    repo = UserProfileRepository(db)
    profile = repo.create_or_update_profile(
        user_id=user_id,
        primary_goal=profile_data.primary_goal,
        secondary_goals=profile_data.secondary_goals,
        focus_areas=profile_data.focus_areas,
        priority_order=profile_data.priority_order,
        time_horizon=profile_data.time_horizon
    )
    return profile

@router.get("/{user_id}")
async def get_profile(user_id: int, db: Session = Depends(get_db_session)):
    repo = UserProfileRepository(db)
    profile = repo.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
