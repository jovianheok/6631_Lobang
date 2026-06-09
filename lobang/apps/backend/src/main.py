
from fastapi import FastAPI
from src.deals import router as deals_router

app = FastAPI(title="Lobang API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(deals_router)