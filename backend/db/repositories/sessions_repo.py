"""Session repository for database operations."""
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from backend.db.connection import get_db_connection, close_db_connection
from backend.utils.password import generate_token


class SessionRepository:
    """Repository for session database operations."""
    
    @staticmethod
    def create_session(
        user_id: int,
        expires_in_hours: int = 24
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new session for a user.
        
        Args:
            user_id: User ID
            expires_in_hours:  Session expiration time in hours
            
        Returns:
            Session dictionary or None if error
        """
        try:
            conn = get_db_connection()
            if not conn:
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            token = generate_token()
            expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
            
            query = """
                INSERT INTO sessions (user_id, session_token, expires_at)
                VALUES (%s, %s, %s)
                RETURNING id, user_id, session_token, expires_at, created_at;
            """
            
            cur.execute(query, (user_id, token, expires_at))
            session = cur.fetchone()
            conn.commit()
            cur.close()
            close_db_connection(conn)
            
            return dict(session) if session else None
            
        except psycopg2.Error as e:
            print(f"❌ Database error creating session: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    @staticmethod
    def get_session(token: str) -> Optional[Dict[str, Any]]:
        """
        Get session by token. 
        
        Args:
            token: Session token
            
        Returns:
            Session dictionary or None if not found or expired
        """
        try: 
            conn = get_db_connection()
            if not conn: 
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            query = """
                SELECT id, user_id, session_token, expires_at, created_at
                FROM sessions
                WHERE session_token = %s AND expires_at > CURRENT_TIMESTAMP;
            """
            
            cur.execute(query, (token,))
            session = cur.fetchone()
            cur.close()
            close_db_connection(conn)
            
            return dict(session) if session else None
            
        except psycopg2.Error as e:
            print(f"❌ Database error fetching session: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    @staticmethod
    def get_user_sessions(user_id: int) -> List[Dict[str, Any]]:
        """
        Get all active sessions for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of session dictionaries
        """
        try: 
            conn = get_db_connection()
            if not conn: 
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            query = """
                SELECT id, user_id, session_token, expires_at, created_at
                FROM sessions
                WHERE user_id = %s AND expires_at > CURRENT_TIMESTAMP
                ORDER BY created_at DESC;
            """
            
            cur.execute(query, (user_id,))
            sessions = cur.fetchall()
            cur.close()
            close_db_connection(conn)
            
            return [dict(s) for s in sessions]
            
        except psycopg2.Error as e:
            print(f"❌ Database error fetching sessions: {str(e)}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return []
    
    @staticmethod
    def delete_session(token: str) -> bool:
        """
        Delete a session. 
        
        Args:
            token: Session token
            
        Returns:
            True if deleted, False otherwise
        """
        try: 
            conn = get_db_connection()
            if not conn: 
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            query = "DELETE FROM sessions WHERE session_token = %s;"
            cur.execute(query, (token,))
            
            deleted = cur.rowcount > 0
            conn.commit()
            cur.close()
            close_db_connection(conn)
            
            return deleted
            
        except psycopg2.Error as e:
            print(f"❌ Database error deleting session: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error:  {str(e)}")
            return False
    
    @staticmethod
    def delete_expired_sessions() -> int:
        """
        Delete all expired sessions.
        
        Returns:
            Number of deleted sessions
        """
        try:
            conn = get_db_connection()
            if not conn:
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            query = "DELETE FROM sessions WHERE expires_at <= CURRENT_TIMESTAMP;"
            cur.execute(query)
            
            deleted_count = cur.rowcount
            conn.commit()
            cur.close()
            close_db_connection(conn)
            
            return deleted_count
            
        except psycopg2.Error as e:
            print(f"❌ Database error deleting sessions: {str(e)}")
            return 0
        except Exception as e:
            print(f"❌ Unexpected error:  {str(e)}")
            return 0