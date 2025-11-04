from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# ✅ Load .env (for DATABASE_URL)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app@127.0.0.1:5432/papers")

# ✅ Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# ✅ Create a configured session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for all ORM models
Base = declarative_base()

# ✅ Dependency that provides a DB session to routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

