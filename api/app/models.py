from sqlalchemy import Column, Integer, String, Date
from .db import Base

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    authors = Column(String, nullable=False)
    published = Column(Date)
    url = Column(String)
    source = Column(String)

