from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.analytics.engine import AnalyticsEngine
from backend.db.repositories.user_profile_repo import UserProfileRepository
from backend.db.repositories.activity_log_repo import ActivityLogRepository
from backend.db.repositories.activity_types_repo import ActivityTypesRepository
from backend.agents.supervisor import SupervisorAgent
import re

router = APIRouter()

from backend.agents.reasoning import ReasoningAgent
from backend.agents.reflection import ReflectionAgent

from backend.db.repositories.summary_repo import AnalyticsSummaryRepository
from backend.db.repositories.chat_repo import ChatRepository
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

    # Save User message to DB and get context
    chat_repo = ChatRepository(db)
    chat_repo.save_message(user_id, "user", query)
    recent_chat = chat_repo.get_recent_context(user_id, limit=6)
    chat_context = [{"role": m.role, "content": m.content} for m in reversed(recent_chat)]

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
            history=history,
            chat_context=chat_context
        )
        # Save AI message to DB
        chat_repo.save_message(user_id, "ai", onboarding_msg)
        
        return {
            "status": "DATA_INSUFFICIENT",
            "message": onboarding_msg,
            "confidence": check.confidence
        }

    # 3. Reasoning Phase (With History, Chat Context and Query)
    reasoner = ReasoningAgent()
    draft = reasoner.generate_guidance(profile, stats, historical_summaries=history, chat_context=chat_context)

    # 4. Reflection Phase (Audit)
    reflector = ReflectionAgent()
    audit = reflector.review_response(draft, profile)

    # 5. Final Output Logic
    if audit.decision == "REJECT":
        return {"status": "INTERNAL_ERROR", "message": "The AI response failed safety checks."}
    
    final_response = audit.suggested_revision if audit.decision == "SOFTEN" else draft

    # 6. Auto-Logging Detection (The "Magic" Link)
    try:
        auto_log_match = re.search(r"\[AUTO_LOG: (.*?), (\d+), (.*?)\]", final_response)
        if auto_log_match:
            act_name = auto_log_match.group(1).strip()
            act_duration = int(auto_log_match.group(2).strip())
            act_notes = auto_log_match.group(3).strip()
            
            # Clean the visible response from the technical tag
            final_response = final_response.replace(auto_log_match.group(0), "").strip()
            
            # Save Log automatically
            types_repo = ActivityTypesRepository(db)
            log_repo = ActivityLogRepository(db)
            act_type = types_repo.get_activity_type_by_name(act_name)
            
            # If not found exactly, try fuzzy matching or default to 'Personal'
            if not act_type:
                act_type = types_repo.get_activity_type_by_name("Personal")

            if act_type:
                log_repo.create_log(
                    user_id=user_id,
                    activity_id=act_type.activity_id,
                    date=datetime.utcnow(),
                    duration_minutes=act_duration,
                    notes=f"(Chat-Sync) {act_notes}",
                    completed=True
                )
    except Exception as e:
        print(f"Auto-log parsing failed: {e}")

    # 7. Profile Update Detection
    try:
        profile_match = re.search(r"\[UPDATE_PROFILE: (.*?), (.*?)\]", final_response)
        if profile_match:
            new_goal = profile_match.group(1).strip()
            new_focus = profile_match.group(2).strip()
            
            # Clean the visible response
            final_response = final_response.replace(profile_match.group(0), "").strip()
            
            update_data = {}
            if new_goal: update_data["primary_goal"] = new_goal
            if new_focus: update_data["focus_areas"] = [f.strip() for f in new_focus.split(",")]
            
            if update_data:
                profile_repo.create_or_update_profile(user_id=user_id, **update_data)
    except Exception as e:
        print(f"Profile update parsing failed: {e}")

    # Save to history
    summary_repo.create_summary(
        user_id=user_id,
        period_type="query_response",
        period_start=datetime.utcnow(),
        period_end=datetime.utcnow(),
        focus_distribution=stats.get("activity_distribution"),
        key_insight=final_response
    )

    # Save AI response to DB
    chat_repo.save_message(user_id, "ai", final_response)

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

@router.get("/history")
async def get_chat_history(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """Returns the chat history for the current user."""
    chat_repo = ChatRepository(db)
    messages = chat_repo.get_history(current_user.user_id)
    return [
        {
            "id": str(m.message_id),
            "role": m.role,
            "content": m.content,
            "timestamp": m.timestamp.isoformat()
        } for m in messages
    ]
