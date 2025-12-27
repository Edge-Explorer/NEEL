"""Activity repository for database operations."""
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any, List
import json

from backend.db.connection import get_db_connection, close_db_connection


class ActivityRepository:
    """Repository for activity log database operations."""
    
    @staticmethod
    def log_activity(
        user_id: int,
        activity_type: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]: 
        """
        Log an activity for a user.
        
        Args:
            user_id:  User ID
            activity_type:  Type of activity (study, exercise, sleep, etc.)
            description: Activity description
            metadata: Optional metadata as dictionary
            
        Returns:
            Activity dictionary or None if error
        """
        try:
            conn = get_db_connection()
            if not conn:
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            metadata_json = json.dumps(metadata) if metadata else None
            
            query = """
                INSERT INTO activity_logs (user_id, activity_type, description, metadata)
                VALUES (%s, %s, %s, %s)
                RETURNING id, user_id, activity_type, description, metadata, created_at;
            """
            
            cur. execute(query, (user_id, activity_type, description, metadata_json))
            activity = cur.fetchone()
            conn.commit()
            cur.close()
            close_db_connection(conn)
            
            return dict(activity) if activity else None
            
        except psycopg2.Error as e:
            print(f"❌ Database error logging activity: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    @staticmethod
    def get_user_activities(
        user_id: int,
        limit: int = 100,
        offset: int = 0,
        activity_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get user's activities.
        
        Args:
            user_id: User ID
            limit: Number of records to fetch
            offset: Offset for pagination
            activity_type: Filter by type (optional)
            
        Returns: 
            List of activity dictionaries
        """
        try:
            conn = get_db_connection()
            if not conn:
                raise Exception("Failed to get database connection")
            
            cur = conn. cursor()
            
            if activity_type:
                query = """
                    SELECT id, user_id, activity_type, description, metadata, created_at
                    FROM activity_logs
                    WHERE user_id = %s AND activity_type = %s
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s;
                """
                cur.execute(query, (user_id, activity_type, limit, offset))
            else:
                query = """
                    SELECT id, user_id, activity_type, description, metadata, created_at
                    FROM activity_logs
                    WHERE user_id = %s
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s;
                """
                cur.execute(query, (user_id, limit, offset))
            
            activities = cur.fetchall()
            cur.close()
            close_db_connection(conn)
            
            return [dict(a) for a in activities]
            
        except psycopg2.Error as e:
            print(f"❌ Database error fetching activities: {str(e)}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return []
    
    @staticmethod
    def get_activity_by_id(activity_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific activity by ID.
        
        Args:
            activity_id: Activity ID
            
        Returns:
            Activity dictionary or None if not found
        """
        try:
            conn = get_db_connection()
            if not conn:
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            query = """
                SELECT id, user_id, activity_type, description, metadata, created_at
                FROM activity_logs
                WHERE id = %s;
            """
            
            cur. execute(query, (activity_id,))
            activity = cur. fetchone()
            cur.close()
            close_db_connection(conn)
            
            return dict(activity) if activity else None
            
        except psycopg2.Error as e:
            print(f"❌ Database error fetching activity: {str(e)}")
            return None
        except Exception as e: 
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    @staticmethod
    def get_activity_summary(
        user_id: int,
        days: int = 7
    ) -> Dict[str, int]:
        """
        Get activity summary for user over specified days.
        
        Args:
            user_id: User ID
            days: Number of days to include
            
        Returns:
            Dictionary with activity counts by type
        """
        try: 
            conn = get_db_connection()
            if not conn: 
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            query = """
                SELECT activity_type, COUNT(*) as count
                FROM activity_logs
                WHERE user_id = %s 
                AND created_at >= CURRENT_TIMESTAMP - INTERVAL '%s days'
                GROUP BY activity_type
                ORDER BY count DESC;
            """
            
            cur. execute(query, (user_id, days))
            results = cur.fetchall()
            cur.close()
            close_db_connection(conn)
            
            summary = {row['activity_type']: row['count'] for row in results}
            return summary
            
        except psycopg2.Error as e:
            print(f"❌ Database error fetching summary:  {str(e)}")
            return {}
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return {}
    
    @staticmethod
    def delete_activity(activity_id: int, user_id: int) -> bool:
        """
        Delete an activity. 
        
        Args:
            activity_id: Activity ID
            user_id: User ID (for validation)
            
        Returns: 
            True if deleted, False otherwise
        """
        try:
            conn = get_db_connection()
            if not conn:
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            query = "DELETE FROM activity_logs WHERE id = %s AND user_id = %s;"
            cur. execute(query, (activity_id, user_id))
            
            deleted = cur.rowcount > 0
            conn.commit()
            cur.close()
            close_db_connection(conn)
            
            return deleted
            
        except psycopg2.Error as e:
            print(f"❌ Database error deleting activity: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return False