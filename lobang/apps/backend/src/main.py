"""
Purpose: Create the FastAPI application and register all routers/endpoints so the backend can receive and handle HTTP requests
"""
import os
from fastapi import FastAPI     # for FastAPI framework
from fastapi.middleware.cors import CORSMiddleware
from src.routes.preference_routes import preference_router
from src.routes.bookmark_routes import bookmark_router
from src.routes.deal_routes  import deal_router
from src.routes.submission_routes import submission_router
from src.routes.vote_routes import vote_router

app = FastAPI(title="Lobang API")       # Create a FastAPI application

# Origins allowed to call this API from the browser. Without this, cross-origin
# fetches are blocked and the UI silently shows no data. Local dev is always
# allowed; every Vercel preview/production URL (https://<something>.vercel.app)
# is matched by regex so the deployed frontend works without re-deploying the
# backend. Extra explicit origins (e.g. a custom domain) can be supplied via the
# FRONTEND_ORIGINS env var (comma-separated) with no code change.
_default_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
_extra_origins = [o.strip() for o in os.getenv("FRONTEND_ORIGINS", "").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_default_origins + _extra_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
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
