"""
Purpose: Create the FastAPI application and register all routers/endpoints so the backend can receive and handle HTTP requests
"""
from fastapi import FastAPI     # for FastAPI framework
from src.routes.preference_routes import preference_router
from src.routes.bookmark_routes import bookmark_router
from src.routes.deal_routes  import deal_router

app = FastAPI(title="Lobang API")       # Create a FastAPI application

@app.get("/")
def root():
    return {"message": "Lobang API is running"}

@app.get("/health")     # Health-check endpoint
def health_check():
    return {"status": "ok"}     # API heakth response

app.include_router(deal_router, prefix="/api/v1")
app.include_router(preference_router, prefix="/api/v1")
app.include_router(bookmark_router, prefix="/api/v1")
