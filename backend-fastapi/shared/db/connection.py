# shared/db/connection.py
import psycopg2
import os

def get_db_connection():
    """Get a database connection using environment variables"""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "wishi"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password"),
        host=os.getenv("DB_HOST", "postgres")
    )