from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Paper

router = APIRouter()

@router.get("/papers")
def list_papers(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: Session = Depends(get_db)):
    total = db.query(Paper).count()
    papers = db.query(Paper).offset(skip).limit(limit).all()
    return {"results": papers, "total": total}

