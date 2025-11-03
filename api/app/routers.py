from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.db import SessionLocal
from app.models import Paper

router = APIRouter(prefix="/api", tags=["papers"])

# Dependency: create and close DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/papers")
def list_papers(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    papers = db.query(Paper).offset(offset).limit(limit).all()
    total = db.query(Paper).count()
    return {"results": papers, "total": total}

@router.post("/papers")
def create_paper(paper: dict, db: Session = Depends(get_db)):
    new_paper = Paper(
        title=paper["title"],
        authors=paper["authors"],
        published=date.fromisoformat(paper["published"]),
        url=paper["url"],
        source=paper["source"],
    )
    db.add(new_paper)
    db.commit()
    db.refresh(new_paper)
    return new_paper

