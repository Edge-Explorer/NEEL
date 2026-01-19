from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.models import ActivityLog, Outcome, Activity

class AnalyticsEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_summary_for_period(self, user_id: int, days: int = 7) -> Dict[str, Any]:
        """
        Aggregates raw data into a structured format for AI agents.
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Fetch data
        logs = self.db.query(ActivityLog, Activity).join(Activity).filter(
            ActivityLog.user_id == user_id,
            ActivityLog.date >= start_date
        ).all()
        
        outcomes = self.db.query(Outcome).filter(
            Outcome.user_id == user_id,
            Outcome.date >= start_date
        ).all()

        # Aggregate Metrics
        activity_stats = {}
        total_minutes = 0
        
        for log, activity in logs:
            cat = activity.activity_category.value
            dur = log.duration_minutes or 0
            activity_stats[cat] = activity_stats.get(cat, 0) + dur
            total_minutes += dur

        outcome_history = [
            {"type": o.outcome_type.value, "value": o.outcome_value, "date": o.date.isoformat()}
            for o in outcomes
        ]

        return {
            "period_days": days,
            "total_active_minutes": total_minutes,
            "activity_distribution": activity_stats,
            "outcome_count": len(outcomes),
            "recent_outcomes": outcome_history
        }
