from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session, engine
from backend.db import Base
from backend.models import User # Ensure models are loaded
import uvicorn

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic (if any) can go here

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="NEEL - Unified Activity & Behavior API",
    description="Unified Backend for AI-driven Life Analytics",
    version="1.0.0",
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

@app.get("/")
def read_root():
    return {"message": "Welcome to NEEL - Unified Activity & Behavior API"}

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
