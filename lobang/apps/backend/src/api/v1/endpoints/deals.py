"""
API routes for deals endpoints.
"""

# FastAPI router for grouping related endpoints
from fastapi import APIRouter

# Pydantic response schema/model
# Defines the shape of returned deal data
from src.schemas.deal import DealOut

# Service function that retrieves deals from database
from src.services.deal_service import get_deals

# Create API router instance
router = APIRouter() 


@router.get("/deals", response_model=list[DealOut])
def list_deals():
    """
    GET /deals

    Returns a list of deals.

    response_model:
    - Ensures returned data matches DealOut schema
    - Automatically generates API documentation
    - Validates response structure
    """

    # Fetch and return deals from service layer
    return get_deals()