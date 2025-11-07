from sqlalchemy import Column, Integer, String, Date
from app.db import Base 
from pydantic import BaseModel
from datetime import date
from sqlalchemy import Column, Integer, String, DateTime, Text


# --- SQLAlchemy model (for DB table) ---
class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    authors = Column(String, nullable=False)
    published = Column(Date, nullable=False)
    url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    thumbnail = Column(String, nullable=True)


# --- Pydantic schemas (for API I/O) ---
class PaperCreate(BaseModel):
    title: str
    authors: str
    published: date
    url: str
    source: str

class PaperRead(PaperCreate):
    id: int

    class Config:
        orm_mode = True

