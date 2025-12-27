import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    """
    Returns a PostgreSQL connection using environment variables. 
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "neel_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "password"),
            cursor_factory=RealDictCursor
        )
        # Set the search_path to public schema
        cur = conn.cursor()
        cur.execute("SET search_path TO public")
        cur.close()
        return conn
    except Exception as e:
        print(f"❌ DB Connection Failed: {str(e)}")
        return None


def close_db_connection(conn):
    """
    Close database connection safely.
    """
    if conn:
        try:
            conn.close()
        except Exception as e:
            print(f"❌ Error closing connection: {str(e)}")