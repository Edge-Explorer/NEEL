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
            "activity_name": log.activity.activity_name if log.activity else "Unknown Activity",
            "timestamp": log.created_at.isoformat() if log.created_at else log.date.isoformat(),
            "date": log.date.isoformat(),
            "duration": log.duration_minutes,
            "notes": log.notes,
            "can_edit": (datetime.utcnow() - log.created_at).total_seconds() < 86400 if log.created_at else True
        })
    
    # 2. User Profile
    profile_repo = UserProfileRepository(db)
    profile = profile_repo.get_profile(user_id)
    
    # 3. Recent Outcomes (Goals)
    outcome_repo = OutcomeRepository(db)
    outcomes = outcome_repo.get_user_outcomes(user_id, limit=5)
    
    # 4. Analytics (Streak & Onboarding)
    engine = AnalyticsEngine(db)
    onboarding = engine.get_onboarding_status(user_id)
    summary = engine.get_summary_for_period(user_id, days=7)
    
    # Calculate Goals Count: Primary Goal (1) + Outcomes
    goals_count = (1 if profile and profile.primary_goal else 0) + len(outcomes)
    
    return {
        "profile": {
            "name": current_user.name,
            "primary_goal": profile.primary_goal if profile else "No primary goal",
            "focus_areas": profile.focus_areas if profile else []
        },
        "activities": activities,
        "outcomes": [
            {"id": o.outcome_id, "type": o.outcome_type.value, "value": o.outcome_value, "date": o.date.isoformat()}
            for o in outcomes
        ],
        "onboarding": onboarding,
        "streak": summary["streak_count"],
        "activity_distribution": summary["activity_distribution"],
        "goals_count": goals_count,
        "last_sync": datetime.utcnow().isoformat(),
        "user_name": current_user.name
    }
