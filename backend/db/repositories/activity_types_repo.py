from sqlalchemy.orm import Session
from backend.models import Activity, ActivityCategory
from typing import List, Optional

class ActivityTypesRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_activity_type(self, name: str, category: ActivityCategory) -> Activity:
        db_activity = Activity(activity_name=name, activity_category=category)
        self.db.add(db_activity)
        self.db.commit()
        self.db.refresh(db_activity)
        return db_activity

    def get_all_activity_types(self) -> List[Activity]:
        return self.db.query(Activity).all()

    def get_activity_type_by_name(self, name: str) -> Optional[Activity]:
        return self.db.query(Activity).filter(Activity.activity_name == name).first()
