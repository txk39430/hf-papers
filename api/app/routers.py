from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
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

# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def list_papers(
    q: str | None = Query(None, description="Search keyword"),
    source: str | None = Query(None, description="Filter by source (e.g. arxiv)"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="How many items to skip"),
    db: Session = Depends(get_db),
):
    """
    Returns a list of papers, filtered and paginated.
    """
    query = db.query(PaperModel)

    # Optional keyword search
    if q:
        query = query.filter(
            or_(
                PaperModel.title.ilike(f"%{q}%"),
                PaperModel.authors.ilike(f"%{q}%"),
                PaperModel.source.ilike(f"%{q}%"),
            )
        )

    # Optional source filter
    if source:
        query = query.filter(PaperModel.source.ilike(f"%{source}%"))

    total = query.count()  # total matching records
    papers = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": papers,
    }


# POST stays the same
@router.post("")
def create_paper(paper: Paper, db: Session = Depends(get_db)):
    db_paper = PaperModel(**paper.dict())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

