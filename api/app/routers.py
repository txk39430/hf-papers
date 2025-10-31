from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date

from .db import SessionLocal
from .models import Paper as PaperModel

router = APIRouter(prefix="/api/papers", tags=["papers"])

# Pydantic schema
class Paper(BaseModel):
    title: str
    authors: str | None = None
    published: date | None = None
    url: str | None = None
    source: str | None = None

    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def list_papers(db: Session = Depends(get_db)):
    return db.query(PaperModel).all()

@router.post("")
def create_paper(paper: Paper, db: Session = Depends(get_db)):
    db_paper = PaperModel(**paper.dict())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

