# shared/db/connection.py
import psycopg2
import os
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    """Get a database connection using environment variables"""
    host = os.getenv("DB_HOST", "postgres")
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "wishi"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "password"),
            host=host
        )
        logger.info(f"Database connection established: host={host}")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: host={host} error={e}", exc_info=True)
        raise