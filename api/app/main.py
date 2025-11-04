from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router as papers_router

app = FastAPI(title="HF Papers API")

# Enable CORS so frontend (localhost:3000) can talk to backend (localhost:8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the /api/papers routes
app.include_router(papers_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "HF Papers API is running 🚀"}

