from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.analytics.engine import AnalyticsEngine
from backend.db.repositories.user_profile_repo import UserProfileRepository
from backend.agents.supervisor import SupervisorAgent

router = APIRouter()

from backend.agents.reasoning import ReasoningAgent
from backend.agents.reflection import ReflectionAgent

@router.get("/analyze/{user_id}")
async def analyze_user_data(user_id: int, db: Session = Depends(get_db_session)):
    """
    Full Multi-Agent Pipeline: 
    Supervisor (Gate) -> Reasoning (Brain) -> Reflection (Auditor)
    """
    # 1. Gather Data
    engine = AnalyticsEngine(db)
    stats = engine.get_summary_for_period(user_id)
    
    profile_repo = UserProfileRepository(db)
    profile_db = profile_repo.get_profile(user_id)
    if not profile_db:
        raise HTTPException(status_code=400, detail="User profile missing.")
    
    profile = {
        "primary_goal": profile_db.primary_goal,
        "focus_areas": profile_db.focus_areas
    }

    # 2. Supervisor Gate
    supervisor = SupervisorAgent()
    check = supervisor.evaluate_data(profile, stats)
    
    if not check.allow_reasoning:
        return {
            "status": "DATA_INSUFFICIENT",
            "message": check.reason,
            "confidence": check.confidence
        }

    # 3. Reasoning Phase
    reasoner = ReasoningAgent()
    draft = reasoner.generate_guidance(profile, stats)

    # 4. Reflection Phase (Audit)
    reflector = ReflectionAgent()
    audit = reflector.review_response(draft, profile)

    # 5. Final Output Logic
    if audit.decision == "REJECT":
        return {"status": "INTERNAL_ERROR", "message": "The AI response failed safety checks."}
    
    final_response = audit.suggested_revision if audit.decision == "SOFTEN" else draft

    return {
        "status": "SUCCESS",
        "confidence": check.confidence,
        "analysis": final_response,
        "reflection_audit": audit.critique
    }
