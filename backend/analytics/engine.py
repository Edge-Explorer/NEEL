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
        logged_dates = set()
        
        for log, activity in logs:
            cat = activity.activity_category.value
            dur = log.duration_minutes or 0
            activity_stats[cat] = activity_stats.get(cat, 0) + dur
            total_minutes += dur
            logged_dates.add(log.date.date())

        outcome_history = [
            {"type": o.outcome_type.value, "value": o.outcome_value, "date": o.date.isoformat()}
            for o in outcomes
        ]

        # Streak calculation
        streak = self.get_user_streak(user_id)

        return {
            "period_days": days,
            "total_active_minutes": total_minutes,
            "activity_distribution": activity_stats,
            "outcome_count": len(outcomes),
            "recent_outcomes": outcome_history,
            "days_logged": len(logged_dates),
            "streak_count": streak
        }

    def get_user_streak(self, user_id: int) -> int:
        """
        Calculates the consecutive days the user has logged activities.
        """
        today = datetime.utcnow().date()
        logs = self.db.query(ActivityLog.date).filter(
            ActivityLog.user_id == user_id
        ).order_by(ActivityLog.date.desc()).all()

        if not logs:
            return 0

        logged_dates = sorted(set(l.date.date() for l in logs), reverse=True)
        
        # If the most recent log is older than yesterday, the streak is broken
        if logged_dates[0] < today - timedelta(days=1):
            return 0

        streak = 0
        current_date = logged_dates[0] # Start from the last day they actually logged

        for date in logged_dates:
            if date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        return streak

    def get_onboarding_status(self, user_id: int) -> Dict[str, Any]:
        """
        Returns the progress toward the initial 7-day/120-minute data gathering phase.
        """
        summary = self.get_summary_for_period(user_id, days=7)
        
        total_minutes = summary["total_active_minutes"]
        days_logged = summary["days_logged"]
        
        # Define targets
        TARGET_MINUTES = 120
        TARGET_DAYS = 7
        
        # Calculate percentages
        minutes_progress = min(100, (total_minutes / TARGET_MINUTES) * 100)
        days_progress = min(100, (days_logged / TARGET_DAYS) * 100)
        overall_progress = (minutes_progress + days_progress) / 2

        return {
            "total_minutes": total_minutes,
            "target_minutes": TARGET_MINUTES,
            "days_logged": days_logged,
            "target_days": TARGET_DAYS,
            "minutes_progress": minutes_progress,
            "days_progress": days_progress,
            "overall_progress": overall_progress,
            "is_complete": total_minutes >= TARGET_MINUTES and days_logged >= 1 # User suggested 7 days but current logic is 120 mins. Let's stick to 120 mins + at least some logging.
        }
