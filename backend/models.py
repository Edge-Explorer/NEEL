"""SQLAlchemy ORM models for NEEL entities."""
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Enum, Float, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.db import Base

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    timezone = Column(String, nullable=True)

class UserProfile(Base):
    __tablename__ = "user_profile"
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    primary_goal = Column(String, nullable=False)
    secondary_goals = Column(JSON, nullable=True)
    focus_areas = Column(JSON, nullable=True)
    priority_order = Column(JSON, nullable=True)
    time_horizon = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Activity(Base):
    __tablename__ = "activity"
    activity_id = Column(Integer, primary_key=True, autoincrement=True)
    activity_name = Column(String, nullable=False, unique=True)
    activity_category = Column(String, nullable=False)

class ActivityLog(Base):
    __tablename__ = "activity_log"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activity.activity_id"), nullable=False)
    date = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    planned = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    postponed = Column(Boolean, default=False)
    energy_level = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Outcome(Base):
    __tablename__ = "outcome"
    outcome_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    date = Column(DateTime, nullable=False)
    outcome_type = Column(String, nullable=False)
    outcome_value = Column(Text, nullable=True)
    related_activity_id = Column(Integer, ForeignKey("activity.activity_id"), nullable=True)

class AnalyticsSummary(Base):
    __tablename__ = "analytics_summary"
    summary_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    period_type = Column(String, nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    focus_distribution = Column(JSON, nullable=True)
    activity_balance = Column(JSON, nullable=True)
    goal_alignment = Column(Text, nullable=True)
    key_insight = Column(Text, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow)