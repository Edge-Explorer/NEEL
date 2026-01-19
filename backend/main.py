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
    logger.info("🚀 NEEL BACKEND v1.0.5 - INITIALIZING...")
    try:
        logger.info("📡 DB CONNECTION START...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ DB TABLES READY.")
    except Exception as e:
        logger.error(f"❌ DB ERROR: {str(e)}")
    yield
    logger.info("🛑 NEEL BACKEND SHUTTING DOWN...")

app = FastAPI(
    title="NEEL - Unified Activity & Behavior API",
    description="Unified Backend for AI-driven Life Analytics",
    version="1.0.5",
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

# Root route - explicitly supporting HEAD for Render
@app.api_route("/", methods=["GET", "HEAD"])
async def read_root(request: Request):
    return {
        "status": "online",
        "message": "Welcome to NEEL - Unified Activity & Behavior API",
        "version": "1.0.5",
        "method": request.method
    }

# Health Check - explicitly supporting HEAD for Render
@app.api_route("/api/health", methods=["GET", "HEAD"])
async def health_check(request: Request):
    return {"status": "healthy", "service": "NEEL", "method": request.method}

# Include routers
from backend.routers import activities, activity_types, profiles, outcomes, intelligence, auth, dashboard
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
app.include_router(activity_types.router, prefix="/api/activity-types", tags=["activity-types"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["profiles"])
app.include_router(outcomes.router, prefix="/api/outcomes", tags=["outcomes"])
app.include_router(intelligence.router, prefix="/api/intelligence", tags=["intelligence"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
