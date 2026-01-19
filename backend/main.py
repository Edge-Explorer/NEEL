from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session, engine
from backend.db import Base
from backend.models import User # Ensure models are loaded
import uvicorn

app = FastAPI(
    title="NEEL API",
    description="Unified Activity & Behavior Schema Backend",
    version="1.0.0"
)

# Create tables on startup (In production, use migrations)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to NEEL - Unified Activity & Behavior API"}

# Include routers
from backend.routers import activities, activity_types, profiles, outcomes, intelligence
app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
app.include_router(activity_types.router, prefix="/api/activity-types", tags=["activity-types"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["profiles"])
app.include_router(outcomes.router, prefix="/api/outcomes", tags=["outcomes"])
app.include_router(intelligence.router, prefix="/api/intelligence", tags=["intelligence"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
