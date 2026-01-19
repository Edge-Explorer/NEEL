from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.models import User
from backend.utils.password import hash_password, verify_password
from backend.utils.auth import create_access_token
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    timezone: Optional[str] = "UTC"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db_session)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hash_password(user_data.password),
        timezone=user_data.timezone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create default profile
    from backend.models import UserProfile
    default_profile = UserProfile(
        user_id=new_user.user_id,
        primary_goal="Set your first goal",
        time_horizon="Monthly"
    )
    db.add(default_profile)
    db.commit()
    
    return {"message": "User created successfully", "user_id": new_user.user_id}

@router.post("/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.user_id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.user_id}

from backend.utils.auth import get_current_user
@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.user_id, "email": current_user.email, "name": current_user.name}
