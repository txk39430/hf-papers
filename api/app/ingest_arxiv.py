import requests
import xml.etree.ElementTree as ET
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Paper

# Example: get top 10 recent papers from arXiv (AI category)
ARXIV_URL = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=10"

def fetch_arxiv_papers():
    print("Fetching papers from arXiv...")
    response = requests.get(ARXIV_URL)
    if response.status_code != 200:
        print("❌ Failed to fetch:", response.status_code)
        return []

    # Parse XML
    root = ET.fromstring(response.content)
    ns = {"arxiv": "http://www.w3.org/2005/Atom"}

    papers = []
    for entry in root.findall("arxiv:entry", ns):
        title = entry.find("arxiv:title", ns).text.strip()
        authors = "; ".join([a.find("arxiv:name", ns).text for a in entry.findall("arxiv:author", ns)])
        published = entry.find("arxiv:published", ns).text.split("T")[0]
        url = entry.find("arxiv:id", ns).text
        papers.append({
            "title": title,
            "authors": authors,
            "published": published,
            "url": url,
            "source": "arxiv"
        })
    return papers

def save_papers_to_db(papers):
    db: Session = SessionLocal()
    for p in papers:
        # Skip duplicates
        exists = db.query(Paper).filter_by(title=p["title"]).first()
        if exists:
            continue
        paper = Paper(**p)
        db.add(paper)
    db.commit()
    db.close()
    print(f"✅ Saved {len(papers)} papers.")

if __name__ == "__main__":
    papers = fetch_arxiv_papers()
    save_papers_to_db(papers)

