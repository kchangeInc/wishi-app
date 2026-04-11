# shared/db/session.py
"""Database session management using SQLAlchemy"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

# Build database URL from environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{os.getenv('DB_USER', 'user')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'postgres')}:5432/{os.getenv('DB_NAME', 'wishi')}"
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=50,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true"  # Debug mode
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session() -> Session:
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables"""
    from shared.models import Base
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all tables (caution! use only in dev/testing)"""
    from shared.models import Base
    Base.metadata.drop_all(bind=engine)
