from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.analytics.engine import AnalyticsEngine
from backend.db.repositories.user_profile_repo import UserProfileRepository
from backend.agents.supervisor import SupervisorAgent

router = APIRouter()

from backend.agents.reasoning import ReasoningAgent
from backend.agents.reflection import ReflectionAgent

from backend.db.repositories.summary_repo import AnalyticsSummaryRepository
from datetime import datetime, timedelta
from pydantic import BaseModel
from backend.utils.auth import get_current_user
from backend.models import User

class QueryRequest(BaseModel):
    query: str

@router.post("/analyze")
async def analyze_with_query(
    request: QueryRequest, 
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    POST version of analyze that takes a query from the user.
    """
    user_id = current_user.user_id
    query = request.query
    
    # 1. Gather Data & History
    engine = AnalyticsEngine(db)
    stats = engine.get_summary_for_period(user_id)
    
    summary_repo = AnalyticsSummaryRepository(db)
    past_summaries = summary_repo.get_latest_summaries(user_id, limit=3)
    history = [{"date": s.generated_at.date().isoformat(), "insight": s.key_insight} for s in past_summaries]

    profile_repo = UserProfileRepository(db)
    profile_db = profile_repo.get_profile(user_id)
    if not profile_db:
        # Create a default profile if it doesn't exist to avoid error
        profile_db = profile_repo.create_or_update_profile(
            user_id=user_id,
            primary_goal="Improve productivity",
            focus_areas=["Work", "Learning"]
        )
    
    profile = {
        "primary_goal": profile_db.primary_goal,
        "focus_areas": profile_db.focus_areas,
        "user_query": query # Pass the query to agents
    }

    # 2. Supervisor Gate
    supervisor = SupervisorAgent()
    check = supervisor.evaluate_data(profile, stats)
    
    if not check.allow_reasoning:
        reasoner = ReasoningAgent()
        onboarding_msg = reasoner.generate_onboarding_guidance(
            check_reason=check.reason, 
            query=query,
            analytics=stats,
            history=history
        )
        return {
            "status": "DATA_INSUFFICIENT",
            "message": onboarding_msg,
            "confidence": check.confidence
        }

    # 3. Reasoning Phase (With History and Query)
    reasoner = ReasoningAgent()
    draft = reasoner.generate_guidance(profile, stats, historical_summaries=history)

    # 4. Reflection Phase (Audit)
    reflector = ReflectionAgent()
    audit = reflector.review_response(draft, profile)

    # 5. Final Output Logic
    if audit.decision == "REJECT":
        return {"status": "INTERNAL_ERROR", "message": "The AI response failed safety checks."}
    
    final_response = audit.suggested_revision if audit.decision == "SOFTEN" else draft

    # Save to history
    summary_repo.create_summary(
        user_id=user_id,
        period_type="query_response",
        period_start=datetime.utcnow(),
        period_end=datetime.utcnow(),
        focus_distribution=stats.get("activity_distribution"),
        key_insight=final_response
    )

    return {
        "status": "SUCCESS",
        "confidence": check.confidence,
        "analysis": final_response,
        "reflection_audit": audit.critique
    }

@router.get("/analyze/{user_id}")
async def analyze_user_data(user_id: int, db: Session = Depends(get_db_session)):
    """
    Full Multi-Agent Pipeline: 
    Supervisor (Gate) -> Reasoning (Brain) -> Reflection (Auditor)
    Now with Historical Memory.
    """
    # 1. Gather Data & History
    engine = AnalyticsEngine(db)
    stats = engine.get_summary_for_period(user_id)
    
    summary_repo = AnalyticsSummaryRepository(db)
    past_summaries = summary_repo.get_latest_summaries(user_id, limit=3)
    history = [{"date": s.generated_at.date().isoformat(), "insight": s.key_insight} for s in past_summaries]

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

    # 3. Reasoning Phase (With History)
    reasoner = ReasoningAgent()
    draft = reasoner.generate_guidance(profile, stats, historical_summaries=history)

    # 4. Reflection Phase (Audit)
    reflector = ReflectionAgent()
    audit = reflector.review_response(draft, profile)

    # 5. Final Output Logic & Saving Memory
    if audit.decision == "REJECT":
        return {"status": "INTERNAL_ERROR", "message": "The AI response failed safety checks."}
    
    final_response = audit.suggested_revision if audit.decision == "SOFTEN" else draft

    # Auto-save this insight as a new summary (Memory for next time)
    summary_repo.create_summary(
        user_id=user_id,
        period_type="weekly",
        period_start=datetime.utcnow() - timedelta(days=7),
        period_end=datetime.utcnow(),
        focus_distribution=stats.get("activity_distribution"),
        key_insight=final_response
    )

    return {
        "status": "SUCCESS",
        "confidence": check.confidence,
        "analysis": final_response,
        "reflection_audit": audit.critique
    }
