from backend.db.connection import SessionLocal
from backend.db.repositories.activity_types_repo import ActivityTypesRepository
from backend.models import ActivityCategory

def seed_activity_types():
    db = SessionLocal()
    repo = ActivityTypesRepository(db)
    
    defaults = [
        ("Coding", ActivityCategory.Work),
        ("Deep Work", ActivityCategory.Work),
        ("Research", ActivityCategory.Academic),
        ("Learning", ActivityCategory.Academic),
        ("Meeting", ActivityCategory.Work),
        ("Exercise", ActivityCategory.Health),
        ("Meditation", ActivityCategory.Health),
        ("Reading", ActivityCategory.Personal),
        ("Leisure", ActivityCategory.Leisure)
    ]
    
    for name, cat in defaults:
        if not repo.get_activity_type_by_name(name):
            print(f"Seeding: {name}")
            repo.create_activity_type(name, cat)
    
    db.close()
    print("Seeding complete!")

if __name__ == "__main__":
    seed_activity_types()
