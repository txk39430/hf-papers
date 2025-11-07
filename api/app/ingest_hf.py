import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Paper
from datetime import date

BASE_URL = "https://huggingface.co/papers/month/2025-10"

def fetch_hf_papers():
    print("🔍 Fetching papers from Hugging Face…")
    res = requests.get(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    cards = soup.select("article")  # each paper card
    papers = []

    for card in cards:
        title_tag = card.select_one("h3")
        title = title_tag.text.strip() if title_tag else "Untitled"

        author_tag = card.select_one("p")
        authors = author_tag.text.strip() if author_tag else "Unknown authors"

        link_tag = card.find("a", href=True)
        url = f"https://huggingface.co{link_tag['href']}" if link_tag else None

        # Extract Hugging Face paper ID from URL to build thumbnail
        paper_id = url.split("/")[-1] if url else None
        thumbnail = f"https://huggingface.co/papers/{paper_id}/thumbnail" if paper_id else None

        papers.append({
            "title": title,
            "authors": authors,
            "published": date(2025, 10, 1),
            "url": url,
            "source": "huggingface",
            "summary": None,
            "thumbnail": thumbnail,
        })

    print(f"✅ Found {len(papers)} papers.")
    return papers


def save_papers_to_db(papers):
    db: Session = SessionLocal()
    count = 0
    for p in papers:
        if db.query(Paper).filter_by(title=p["title"]).first():
            continue
        db.add(Paper(**p))
        count += 1
    db.commit()
    db.close()
    print(f"💾 Saved {count} new papers.")


if __name__ == "__main__":
    papers = fetch_hf_papers()
    save_papers_to_db(papers)
