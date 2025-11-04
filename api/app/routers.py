from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Paper, PaperCreate, PaperRead

router = APIRouter()

@router.get("/papers", response_model=list[PaperRead])
def list_papers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    papers = db.query(Paper).offset(skip).limit(limit).all()
    return papers

@router.post("/papers", response_model=PaperRead)
def add_paper(paper: PaperCreate, db: Session = Depends(get_db)):
    new_paper = Paper(**paper.dict())
    db.add(new_paper)
    db.commit()
    db.refresh(new_paper)
    return new_paper



