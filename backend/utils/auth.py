import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-fallback-secret-key-for-dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.db.connection import get_db_session
from backend.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    print(f"DEBUG: get_current_user called with token: {token[:10]}...")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        print("DEBUG: Token decoding failed")
        raise credentials_exception
    print(f"DEBUG: Payload: {payload}")
    user_id: str = payload.get("sub")
    if user_id is None:
        print("DEBUG: sub (user_id) missing from payload")
        raise credentials_exception
    user = db.query(User).filter(User.user_id == int(user_id)).first()
    if user is None:
        print(f"DEBUG: User not found for ID: {user_id}")
        raise credentials_exception
    print(f"DEBUG: User found: {user.email}")
    return user
