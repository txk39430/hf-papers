from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.routers import router as papers_router
from app.ingest_arxiv import fetch_and_store_papers  # ✅ import your existing function

app = FastAPI(title="HF Papers API")

# ✅ Allow frontend (localhost:3000) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routes
app.include_router(papers_router, prefix="/api")

# 🕒 APScheduler setup
scheduler = BackgroundScheduler()

def scheduled_job():
    print(f"🕒 Running daily ingestion at {datetime.now()}")
    try:
        fetch_and_store_papers()  # runs your arXiv ingestion script
        print("✅ Ingestion completed successfully.")
    except Exception as e:
        print("❌ Ingestion failed:", e)

@app.on_event("startup")
def start_scheduler():
    scheduler.add_job(scheduled_job, "interval", days=1)  # run once per day
    scheduler.start()
    print("🚀 APScheduler started...")

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
    print("🛑 Scheduler stopped.")

@app.get("/")
def read_root():
    return {"message": "HF Papers API is running 🚀"}
