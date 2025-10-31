from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Get the database URL and fix the driver for SQLAlchemy
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+psycopg2://")

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)

# Session factory for interacting with the DB
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# Base class for model definitions
class Base(DeclarativeBase):
    pass

