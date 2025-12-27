"""
Test script for database operations. 
Handles duplicate user creation gracefully.
"""
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path. insert(0, str(backend_dir))
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.db.repositories import UserRepository, ActivityRepository, SessionRepository
import psycopg2


def test_create_user(email: str, name: str, password: str = "password123"):
    """
    Create a new user, handling duplicate email gracefully.
    
    Args:
        email: User's email address
        name: User's name
        password: User's password
        
    Returns: 
        User dictionary if successful, None otherwise
    """
    user = UserRepository.get_user_by_email(email)
    
    if user:
        print(f"⚠️  User already exists:  {email}")
        print(f"  Using existing user ID: {user['id']}")
        return user
    
    user = UserRepository.create_user(email, name, password)
    if user:
        print(f"✓ User created successfully: {name} ({email}) - ID: {user['id']}")
    else:
        print(f"✗ Failed to create user: {name}")
    
    return user


def test_log_activity(user_id: int, activity_name: str, activity_type: str, metadata=None):
    """
    Log an activity for a user.
    
    Args:
        user_id: User ID
        activity_name: Name of the activity
        activity_type: Type of activity
        metadata:  Optional metadata dictionary
        
    Returns:
        True if successful, False otherwise
    """
    activity = ActivityRepository.log_activity(
        user_id, 
        activity_type, 
        activity_name, 
        metadata
    )
    
    if activity:
        print(f"✓ Activity logged:  {activity_name} (ID:  {activity['id']})")
        return True
    else: 
        print(f"✗ Failed to log activity: {activity_name}")
        return False


def test_create_session(user_id: int):
    """
    Create a session for a user.
    
    Args:
        user_id:  User ID
        
    Returns: 
        Session dictionary if successful, None otherwise
    """
    session = SessionRepository.create_session(user_id)
    
    if session:
        print(f"✓ Session created for user {user_id}")
        print(f"  Token: {session['session_token'][: 20]}...")
        return session
    else:
        print(f"✗ Failed to create session for user {user_id}")
        return None


def test_get_activity_summary(user_id: int, days: int = 7):
    """
    Get activity summary for a user. 
    
    Args:
        user_id: User ID
        days: Number of days to look back
        
    Returns: 
        Summary dictionary
    """
    summary = ActivityRepository.get_activity_summary(user_id, days)
    
    if summary:
        print(f"✓ Activity summary (last {days} days):")
        for activity_type, count in summary.items():
            print(f"  - {activity_type}: {count}")
        return summary
    else: 
        print(f"ℹ️  No activities found for user {user_id}")
        return {}


def main():
    """Main test function."""
    print("=" * 60)
    print("NEEL Database Test")
    print("=" * 60)
    
    # Test 1: Create/fetch users
    print("\n[1] Creating/fetching test users...")
    users = [
        ("karan@example.com", "Karan"),
        ("alice@example.com", "Alice"),
        ("bob@example.com", "Bob"),
    ]
    
    user_ids = {}
    for email, name in users:
        user = test_create_user(email, name)
        if user:
            user_ids[name] = user['id']
    
    if not user_ids:
        print("\n✗ No users available.  Exiting.")
        return
    
    # Test 2: Log activities
    print("\n[2] Logging activities...")
    for name, uid in user_ids.items():
        activities = [
            (f"{name}'s morning study", "study", {"duration_minutes": 120, "subject": "Math"}),
            (f"{name}'s exercise", "exercise", {"type": "running", "duration_minutes": 30}),
            (f"{name}'s entertainment", "leisure", {"type": "gaming", "duration_minutes": 60}),
        ]
        
        for activity_name, activity_type, metadata in activities:
            test_log_activity(uid, activity_name, activity_type, metadata)
    
    # Test 3: Create sessions
    print("\n[3] Creating sessions...")
    for name, uid in list(user_ids.items())[:1]: 
        test_create_session(uid)
    
    # Test 4: Get activity summary
    print("\n[4] Getting activity summaries...")
    for name, uid in user_ids.items():
        print(f"\n{name}'s activities:")
        test_get_activity_summary(uid)
    
    print("\n" + "=" * 60)
    print("✓ Test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()