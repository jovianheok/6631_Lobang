"""
Purpose: Store all API endpoints related to deals
"""

from fastapi import APIRouter
from src.schemas.deal_schema import DealOut
from src.services.deal_service import get_deals

deal_router = APIRouter()        # Create a router that will hold all deal-related endpoints

@deal_router.get("/deals", response_model=list[DealOut])        # Register this function as the handler for GET requests to /deals
def list_deals():
    return get_deals()      # FastAPI automatically converts Python objects into JSON before sending to frontend%