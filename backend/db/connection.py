import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Raw Connection info
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "neel_db")
DB_USER = os.getenv("DB_USER", "postgres")
import urllib.parse
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy Setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """
    Dependency to get a SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_connection():
    """
    Returns a PostgreSQL connection using environment variables (psycopg2). 
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
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