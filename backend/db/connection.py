import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Robust pgbouncer stripping
    import re
    DATABASE_URL = re.sub(r'(\?|&)pgbouncer=true', '', DATABASE_URL)
    # If we removed the first param, make sure the next one starts with ? not &
    if '?' not in DATABASE_URL and '&' in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace('&', '?', 1)
    
    logger.info(f"🔌 DB URL Cleaned and Ready")

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
from sqlalchemy.pool import NullPool
try:
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"connect_timeout": 10},
        poolclass=NullPool # Recommended for Supabase Transaction Pooler
    )
    logger.info("✅ Database engine created successfully")
except Exception as e:
    logger.error(f"❌ FAILED to create database engine: {str(e)}")
    # We create a dummy engine to prevent the whole app from crashing on import
    engine = create_engine("sqlite:///:memory:") 

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
            # psycopg2 doesn't like the +psycopg2 prefix that SQLAlchemy/Alembic use
            if "postgresql+psycopg2://" in dsn:
                dsn = dsn.replace("postgresql+psycopg2://", "postgresql://", 1)
            elif "postgres+psycopg2://" in dsn:
                dsn = dsn.replace("postgres+psycopg2://", "postgresql://", 1)
            elif dsn.startswith("postgres://"):
                dsn = dsn.replace("postgres://", "postgresql://", 1)
            
            # Strip pgbouncer=true robustly
            import re
            dsn = re.sub(r'(\?|&)pgbouncer=true', '', dsn)
            if '?' not in dsn and '&' in dsn:
                dsn = dsn.replace('&', '?', 1)
                
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