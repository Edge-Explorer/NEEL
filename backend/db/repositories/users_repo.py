"""User repository for database operations."""
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any

from backend.db.connection import get_db_connection, close_db_connection
from backend.utils.password import hash_password, verify_password


class UserRepository:
    """Repository for user database operations."""
    
    @staticmethod
    def create_user(
        email: str,
        name: str,
        password: str
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new user. 
        
        Args:
            email: User's email address
            name: User's name
            password: Plain text password
            
        Returns: 
            User dictionary with id or None if error
        """
        try: 
            conn = get_db_connection()
            if not conn:
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            password_hash = hash_password(password)
            
            query = """
                INSERT INTO users (email, name, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id, email, name, created_at;
            """
            
            cur.execute(query, (email, name, password_hash))
            user = cur.fetchone()
            conn.commit()
            cur.close()
            close_db_connection(conn)
            
            return dict(user) if user else None
            
        except psycopg2.errors.UniqueViolation:
            print(f"⚠️  User already exists: {email}")
            return None
        except psycopg2.Error as e:
            print(f"❌ Database error creating user: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error:  {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email.
        
        Args:
            email: User's email address
            
        Returns: 
            User dictionary or None if not found
        """
        try: 
            conn = get_db_connection()
            if not conn: 
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            query = """
                SELECT id, email, name, password_hash, created_at, updated_at
                FROM users
                WHERE email = %s;
            """
            
            cur.execute(query, (email,))
            user = cur.fetchone()
            cur.close()
            close_db_connection(conn)
            
            return dict(user) if user else None
            
        except psycopg2.Error as e:
            print(f"❌ Database error fetching user: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID. 
        
        Args:
            user_id: User ID
            
        Returns:
            User dictionary or None if not found
        """
        try:
            conn = get_db_connection()
            if not conn:
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            query = """
                SELECT id, email, name, created_at, updated_at
                FROM users
                WHERE id = %s;
            """
            
            cur.execute(query, (user_id,))
            user = cur.fetchone()
            cur.close()
            close_db_connection(conn)
            
            return dict(user) if user else None
            
        except psycopg2.Error as e:
            print(f"❌ Database error fetching user: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    @staticmethod
    def verify_user_password(email: str, password: str) -> Optional[Dict[str, Any]]: 
        """
        Verify user password and return user if valid.
        
        Args:
            email: User's email
            password: Plain text password
            
        Returns:
            User dictionary if valid, None otherwise
        """
        try:
            user = UserRepository.get_user_by_email(email)
            if not user:
                return None
            
            if verify_password(password, user['password_hash']):
                # Remove password hash from response
                user. pop('password_hash', None)
                return user
            
            return None
            
        except Exception as e:
            print(f"❌ Error verifying password: {str(e)}")
            return None
    
    @staticmethod
    def update_user(user_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Update user information.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update (name, email, etc.)
            
        Returns:
            Updated user dictionary or None if error
        """
        try: 
            conn = get_db_connection()
            if not conn: 
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            # Build dynamic query
            allowed_fields = ['name', 'email']
            updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
            
            if not updates:
                return UserRepository.get_user_by_id(user_id)
            
            set_clause = ", ".join([f"{k} = %s" for k in updates. keys()])
            values = list(updates.values()) + [user_id]
            
            query = f"""
                UPDATE users
                SET {set_clause}, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING id, email, name, created_at, updated_at;
            """
            
            cur.execute(query, values)
            user = cur.fetchone()
            conn.commit()
            cur.close()
            close_db_connection(conn)
            
            return dict(user) if user else None
            
        except psycopg2.Error as e:
            print(f"❌ Database error updating user: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False otherwise
        """
        try: 
            conn = get_db_connection()
            if not conn: 
                raise Exception("Failed to get database connection")
            
            cur = conn.cursor()
            
            query = "DELETE FROM users WHERE id = %s;"
            cur. execute(query, (user_id,))
            
            deleted = cur.rowcount > 0
            conn.commit()
            cur.close()
            close_db_connection(conn)
            
            return deleted
            
        except psycopg2.Error as e:
            print(f"❌ Database error deleting user: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return False