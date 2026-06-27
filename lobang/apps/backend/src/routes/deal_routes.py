"""
Purpose: Store all API endpoints related to deals
"""

from fastapi import APIRouter, Depends
from src.auth.supabase_auth import get_current_user
from src.schemas.deal_schema import DealOut
from src.services.deal_service import get_deals, get_for_you_deals

deal_router = APIRouter()        # Create a router that will hold all deal-related endpoints

@deal_router.get("/deals", response_model=list[DealOut])        # Register this function as the handler for GET requests to /deals
def list_deals():
    return get_deals()      # FastAPI automatically converts Python objects into JSON before sending to frontend


@deal_router.get("/deals/for-you", response_model=list[DealOut])
def list_for_you(user_id: str = Depends(get_current_user)):
    """Active deals curated and ranked to the signed-in user's preferences."""
    return get_for_you_deals(user_id)
