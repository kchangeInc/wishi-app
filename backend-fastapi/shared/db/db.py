from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.db.config import build_database_url

DATABASE_URL = build_database_url()

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=50)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()