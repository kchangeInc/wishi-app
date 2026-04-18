# shared/db/session.py
"""Database session management using SQLAlchemy — multi-schema"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
import os
import logging
from shared.db.config import build_database_url

logger = logging.getLogger(__name__)

# Build database URL from environment variables
DATABASE_URL = build_database_url()

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=50,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true"
)
logger.info("Database engine created: pool_size=20 max_overflow=50")

# Set search_path on every new connection so unqualified queries resolve correctly
@event.listens_for(engine, "connect")
def set_search_path(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET search_path TO public, core, ai, company, analytics, automation, seo")
    cursor.close()
    dbapi_connection.commit()

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
