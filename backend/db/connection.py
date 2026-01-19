import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    # Fallback to individual components
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "neel_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    import urllib.parse
    encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
    DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy Setup
# Add a 10 second timeout to connection attempts to prevent hangs
engine = create_engine(
    DATABASE_URL, 
    connect_args={"connect_timeout": 10}
)
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
        # Priority: DATABASE_URL, then individual components
        dsn = os.getenv("DATABASE_URL")
        if dsn:
            conn = psycopg2.connect(dsn, cursor_factory=RealDictCursor)
        else:
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