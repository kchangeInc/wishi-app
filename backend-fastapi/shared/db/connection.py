# shared/db/connection.py
import psycopg2
import logging
from shared.db.config import get_db_settings

logger = logging.getLogger(__name__)

def get_db_connection():
    """Get a database connection using environment variables"""
    settings = get_db_settings()
    host = settings["host"]
    try:
        conn = psycopg2.connect(
            dbname=settings["name"],
            user=settings["user"],
            password=settings["password"],
            host=host,
            port=settings["port"],
        )
        logger.info(f"Database connection established: host={host}")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: host={host} error={e}", exc_info=True)
        raise