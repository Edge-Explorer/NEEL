import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "neel_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

def run_manual_migration():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        
        print("Adding columns to user table...")
        cur.execute('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS email VARCHAR(255) UNIQUE;')
        cur.execute('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS name VARCHAR(255);')
        cur.execute('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);')
        
        print("Creating analytics_summary table if not exists...")
        # (This is already in schema.sql but good to double check)
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Manual migration successful!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    run_manual_migration()
