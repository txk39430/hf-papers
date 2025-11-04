from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router as papers_router

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

@app.get("/")
def read_root():
    return {"message": "HF Papers API is running 🚀"}

