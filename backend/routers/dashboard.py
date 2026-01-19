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
    
    # 1. Recent Stats (Last 7 Days)
    engine = AnalyticsEngine(db)
    weekly_stats = engine.get_summary_for_period(user_id, days=7)
    
    # 2. Today's Logs
    log_repo = ActivityLogRepository(db)
    all_logs = log_repo.get_user_logs(user_id, limit=20)
    today_str = datetime.utcnow().date().isoformat()
    today_logs = [log for log in all_logs if log.date.isoformat() == today_str]
    
    # 3. User Profile
    profile_repo = UserProfileRepository(db)
    profile = profile_repo.get_profile(user_id)
    
    # 4. Recent Outcomes
    outcome_repo = OutcomeRepository(db)
    outcomes = outcome_repo.get_user_outcomes(user_id, limit=5)
    
    return {
        "user_name": current_user.name,
        "weekly_stats": weekly_stats,
        "today_logs_count": len(today_logs),
        "primary_goal": profile.primary_goal if profile else "No goal set",
        "recent_outcomes": [
            {"type": o.outcome_type.value, "value": o.outcome_value, "date": o.date.isoformat()}
            for o in outcomes
        ]
    }
