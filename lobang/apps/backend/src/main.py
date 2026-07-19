"""
Purpose: Create the FastAPI application and register all routers/endpoints so the backend can receive and handle HTTP requests
"""
from fastapi import FastAPI     # for FastAPI framework
from fastapi.middleware.cors import CORSMiddleware
from src.routes.preference_routes import preference_router
from src.routes.bookmark_routes import bookmark_router
from src.routes.deal_routes  import deal_router
from src.routes.submission_routes import submission_router
from src.routes.vote_routes import vote_router

app = FastAPI(title="Lobang API")       # Create a FastAPI application

# Allow the Next.js dev frontend (localhost / 127.0.0.1 on :3000) to call the
# API from the browser. Without this, cross-origin fetches are blocked and the
# UI silently shows no data.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Lobang API is running"}

@app.get("/health")     # Health-check endpoint
def health_check():
    return {"status": "ok"}     # API heakth response

app.include_router(deal_router, prefix="/api/v1")
app.include_router(preference_router, prefix="/api/v1")
app.include_router(bookmark_router, prefix="/api/v1")
app.include_router(submission_router, prefix="/api/v1")
app.include_router(vote_router, prefix="/api/v1")
