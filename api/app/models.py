from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import date

Base = declarative_base()

# --- SQLAlchemy model (for DB table) ---
class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    authors = Column(String, nullable=False)
    published = Column(Date, nullable=False)
    url = Column(String, nullable=False)
    source = Column(String, nullable=False)

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

