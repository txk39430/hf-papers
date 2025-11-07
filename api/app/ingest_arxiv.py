import requests
import xml.etree.ElementTree as ET
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Paper

# Fetch the 10 most recent AI papers from arXiv
ARXIV_URL = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10"


def fetch_arxiv_papers():
    """Fetch and parse papers from the arXiv API."""
    print("📡 Fetching papers from arXiv...")
    response = requests.get(ARXIV_URL)
    if response.status_code != 200:
        print(f"❌ Failed to fetch: {response.status_code}")
        return []

    # Parse XML
    root = ET.fromstring(response.content)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    papers = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        authors = "; ".join(
            [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
        )
        published = entry.find("atom:published", ns).text.split("T")[0]
        url = entry.find("atom:id", ns).text.strip()
        summary = entry.find("atom:summary", ns).text.strip()

        papers.append({
            "title": title,
            "authors": authors,
            "published": published,
            "url": url,
            "source": "arxiv",
            "summary": summary
        })

    print(f"✅ Parsed {len(papers)} papers from arXiv.")
    return papers


def save_papers_to_db(papers):
    """Save fetched papers to the database, skipping duplicates."""
    db: Session = SessionLocal()
    added = 0
    for p in papers:
        exists = db.query(Paper).filter_by(title=p["title"]).first()
        if exists:
            continue
        paper = Paper(**p)
        db.add(paper)
        added += 1
    db.commit()
    db.close()
    print(f"💾 Saved {added} new papers to the database.")


def fetch_and_store_papers():
    """Fetch and save in one go."""
    papers = fetch_arxiv_papers()
    if papers:
        save_papers_to_db(papers)
    else:
        print("⚠️ No papers fetched.")


if __name__ == "__main__":
    fetch_and_store_papers()
