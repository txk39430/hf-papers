from fastapi import FastAPI
from pydantic import BaseModel
import os, psycopg2, redis

# 👇 These two lines read variables from api/.env into your app at startup
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

app = FastAPI(title="HF Papers API", version="0.1.0")

from .routers import router as papers_router
app.include_router(papers_router)


def db_ok() -> bool:
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
        conn.close()
        return True
    except Exception:
        return False

def redis_ok() -> bool:
    try:
        r = redis.Redis.from_url(os.getenv("REDIS_URL"))
        return r.ping()
    except Exception:
        return False

class Health(BaseModel):
    status: str
    db: bool
    redis: bool

@app.get("/health", response_model=Health)
def health():
    return Health(status="ok", db=db_ok(), redis=redis_ok())

@app.get("/api/hello")
def hello():
    return {"message": "FastAPI is running locally 🎉"}
