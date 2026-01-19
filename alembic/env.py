"""Alembic environment configuration.

This module sets up Alembic for database migrations, loading credentials
from environment variables and configuring SQLAlchemy for both online and
offline migration modes. 
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
import os
import sys
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add project root to sys.path so we can import backend modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import Base from backend.db
# This allows Alembic to auto-detect model changes
from backend.db import Base

# IMPORTANT: Import all models so they're registered with Base.metadata
from backend.models import (
    User, UserProfile, Activity, ActivityLog, Outcome, AnalyticsSummary
)

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "neel_db")

# URL-encode password to safely handle special characters (e.g., @, %, : , /)
DB_PASSWORD_ENC = urllib.parse.quote_plus(DB_PASSWORD)

# Build complete database URL for psycopg2
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD_ENC}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ============================================================================
# ALEMBIC CONFIGURATION
# ============================================================================

config = context.config

# Load logging configuration from alembic.ini if it exists
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the SQLAlchemy target metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    """
    context.configure(
        url=SQLALCHEMY_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Create engine directly with the safe URL
    # This bypasses configparser's interpolation issues
    connectable = create_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================================
# EXECUTION
# ============================================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()