from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.analytics.engine import AnalyticsEngine
from backend.db.repositories.user_profile_repo import UserProfileRepository
from backend.agents.supervisor import SupervisorAgent

router = APIRouter()

@router.get("/status/{user_id}")
async def get_ai_status(user_id: int, db: Session = Depends(get_db_session)):
    """
    Analyzes user data through the AI Supervisor gate.
    """
    # 1. Get Analytics
    engine = AnalyticsEngine(db)
    stats = engine.get_summary_for_period(user_id)
    
    # 2. Get Profile
    profile_repo = UserProfileRepository(db)
    profile = profile_repo.get_profile(user_id)
    
    if not profile:
        raise HTTPException(status_code=400, detail="User profile missing. Please set goals first.")

    # 3. Run Supervisor Gate
    supervisor = SupervisorAgent()
    evaluation = supervisor.evaluate_data(
        user_profile={
            "goal": profile.primary_goal,
            "focus": profile.focus_areas
        },
        analytics=stats
    )
    
    return {
        "analytics": stats,
        "supervisor_evaluation": evaluation
    }
