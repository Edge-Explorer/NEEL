from sqlalchemy.orm import Session
from backend.models import UserProfile
from typing import Optional

class UserProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_or_update_profile(self, user_id: int, **kwargs) -> UserProfile:
        db_profile = self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if db_profile:
            for key, value in kwargs.items():
                setattr(db_profile, key, value)
        else:
            db_profile = UserProfile(user_id=user_id, **kwargs)
            self.db.add(db_profile)
        
        self.db.commit()
        self.db.refresh(db_profile)
        return db_profile

    def get_profile(self, user_id: int) -> Optional[UserProfile]:
        return self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
