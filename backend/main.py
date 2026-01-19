from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session, engine
from backend.db import Base
from backend.models import User # Ensure models are loaded
import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    logger.info("🚀 Starting up NEEL Backend...")
    try:
        logger.info("📡 Connecting to Database...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables synchronized.")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
    yield
    logger.info("🛑 Shutting down NEEL Backend...")

app = FastAPI(
    title="NEEL - Unified Activity & Behavior API",
    description="Unified Backend for AI-driven Life Analytics",
    version="1.0.2",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Render-specific Health Check (Allows both GET and HEAD)
@app.api_route("/", methods=["GET", "HEAD"])
def read_root():
    return {
        "status": "online",
        "message": "Welcome to NEEL - Unified Activity & Behavior API",
        "version": "1.0.2"
    }

@app.api_route("/api/health", methods=["GET", "HEAD"])
def health_check():
    return {"status": "healthy", "service": "NEEL"}

# Include routers
try:
    from backend.routers import activities, activity_types, profiles, outcomes, intelligence, auth, dashboard
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
    app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
    app.include_router(activity_types.router, prefix="/api/activity-types", tags=["activity-types"])
    app.include_router(profiles.router, prefix="/api/profiles", tags=["profiles"])
    app.include_router(outcomes.router, prefix="/api/outcomes", tags=["outcomes"])
    app.include_router(intelligence.router, prefix="/api/intelligence", tags=["intelligence"])
    logger.info("✅ All routers included successfully.")
except Exception as e:
    logger.error(f"❌ Failed to include routers: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
