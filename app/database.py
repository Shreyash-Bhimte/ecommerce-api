from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Railway environment variable (if set)
DATABASE_URL = os.getenv("DATABASE_URL")

# If not set, use the Railway PostgreSQL URL directly
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:SHR12febpg@maglev.proxy.rlwy.net:17381/railway"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()