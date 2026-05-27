from fastapi import FastAPI
from src.api.v1.router import api_router

app = FastAPI(title="Lobang API")                       # Creates the real FastAPI app


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/v1")        # Attaches the v1 router