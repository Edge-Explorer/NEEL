from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session, engine
from backend.db import Base
from backend.models import User
import logging

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import activities, activity_types, profiles, outcomes, intelligence, auth, dashboard

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables (Redundant since migrations are already run)
    logger.info("🚀 NEEL CORE v1.0.7 - STARTING")
    # try:
    #     Base.metadata.create_all(bind=engine)
    #     logger.info("✅ DATABASE SYNC COMPLETE")
    # except Exception as e:
    #     logger.error(f"❌ DATABASE ERROR: {str(e)}")

    yield

app = FastAPI(
    title="NEEL",
    version="1.0.7",
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

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"DEBUG: Incoming Request {request.method} {request.url}")
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        import traceback
        print(f"CRITICAL ERROR: {str(e)}\n{traceback.format_exc()}")
        raise e

@app.get("/api/health")
async def health_check():
    from backend.db.connection import engine
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/")
async def root():
    return {"status": "online", "version": "1.0.7", "app": "NEEL"}

@app.head("/")
async def root_head():
    return {}

@app.get("/health")
async def health():
    return {"status": "ok"}

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
app.include_router(activity_types.router, prefix="/api/activity-types", tags=["activity-types"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["profiles"])
app.include_router(outcomes.router, prefix="/api/outcomes", tags=["outcomes"])
app.include_router(intelligence.router, prefix="/api/intelligence", tags=["intelligence"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

