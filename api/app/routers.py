from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/papers", tags=["papers"])

# temporary in-memory "database"
papers = []

class Paper(BaseModel):
    title: str
    authors: str | None = None
    published: str | None = None
    url: str | None = None
    source: str | None = None

@router.get("")
def list_papers():
    return papers

@router.post("")
def create_paper(paper: Paper):
    papers.append(paper)
    return paper

