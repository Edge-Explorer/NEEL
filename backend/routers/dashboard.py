from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.db.connection import get_db_session
from backend.analytics.engine import AnalyticsEngine
from backend.db.repositories.activity_log_repo import ActivityLogRepository
from backend.db.repositories.outcome_repo import OutcomeRepository
from backend.db.repositories.user_profile_repo import UserProfileRepository
from backend.utils.auth import get_current_user
from backend.models import User

router = APIRouter()

@router.get("/")
async def get_dashboard(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    """
    Returns a unified set of data for the frontend dashboard.
    """
    user_id = current_user.user_id
    
    # 1. Activities (Logs) - Fetch actual activity types
    log_repo = ActivityLogRepository(db)
    all_logs = log_repo.get_user_logs(user_id, limit=10)
    
    # Format activities for frontend
    activities = []
    for log in all_logs:
        activities.append({
            "log_id": log.log_id,
            "activity_type": {"name": log.activity.activity_name if log.activity else "Unknown Activity"},
            "timestamp": log.date.isoformat(),
            "date": log.date.isoformat()
        })
    
    # 2. User Profile
    profile_repo = UserProfileRepository(db)
    profile = profile_repo.get_profile(user_id)
    
    # 3. Recent Outcomes (Goals)
    outcome_repo = OutcomeRepository(db)
    outcomes = outcome_repo.get_user_outcomes(user_id, limit=5)
    
    return {
        "profile": {
            "name": current_user.name,
            "primary_goal": profile.primary_goal if profile else "No primary goal"
        },
        "activities": activities,
        "outcomes": [
            {"id": o.outcome_id, "type": o.outcome_type.value, "value": o.outcome_value, "date": o.date.isoformat()}
            for o in outcomes
        ],
        "user_name": current_user.name # Keep for compatibility
    }
