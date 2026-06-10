"""
Purpose: Create the FastAPI application and register all routers/endpoints so the backend can receive and handle HTTP requests
"""
from fastapi import FastAPI     # for FastAPI framework
from src.routes.deal_routes  import deal_router

app = FastAPI(title="Lobang API")       # Create a FastAPI application

@app.get("/")
def root():
    return {"message": "Lobang API is running"}

@app.get("/health")     # Health-check endpoint
def health_check():
    return {"status": "ok"}     # API heakth response

app.include_router(deal_router)     # Register deal endpoints