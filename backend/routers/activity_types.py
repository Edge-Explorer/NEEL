from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.db.repositories.activity_types_repo import ActivityTypesRepository
from backend.models import ActivityCategory
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ActivityTypeCreate(BaseModel):
    name: str
    category: ActivityCategory

@router.post("/")
async def create_activity_type(activity_data: ActivityTypeCreate, db: Session = Depends(get_db_session)):
    repo = ActivityTypesRepository(db)
    if repo.get_activity_type_by_name(activity_data.name):
        raise HTTPException(status_code=400, detail="Activity type already exists")
    return repo.create_activity_type(activity_data.name, activity_data.category)

@router.get("/")
async def get_activity_types(db: Session = Depends(get_db_session)):
    repo = ActivityTypesRepository(db)
    return repo.get_all_activity_types()
