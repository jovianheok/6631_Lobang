"""
Purpose: Store all API endpoints related to deals
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from src.auth.supabase_auth import get_current_user, get_optional_current_user
from src.schemas.deal_schema import DealOut
from src.services.deal_service import get_deals, get_for_you_deals, resolve_deal_image_url

deal_router = APIRouter()        # Create a router that will hold all deal-related endpoints

@deal_router.get("/deals", response_model=list[DealOut])        # Register this function as the handler for GET requests to /deals
def list_deals(user_id: str | None = Depends(get_optional_current_user)):
    return get_deals(user_id)      # FastAPI automatically converts Python objects into JSON before sending to frontend


@deal_router.get("/deals/for-you", response_model=list[DealOut])
def list_for_you(user_id: str = Depends(get_current_user)):
    """Active deals curated and ranked to the signed-in user's preferences."""
    return get_for_you_deals(user_id)


@deal_router.get("/deals/{deal_id}/image")
def get_deal_image(deal_id: int):
    """
    Redirect to the freshest known Telegram image URL for a deal.
    """
    image_url = resolve_deal_image_url(deal_id)
    if not image_url:
        raise HTTPException(status_code=404, detail="Image not found")
    return RedirectResponse(image_url, status_code=307)
