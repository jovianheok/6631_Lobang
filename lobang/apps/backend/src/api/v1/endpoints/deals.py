# Receives HTTP requests -> calls the service -> returns response

from fastapi import APIRouter                           # Imports FastAPI’s router helper.
from src.schemas.deal import DealOut                    # Imports the response schema.
from src.services.deal_service import get_mock_deals    # Imports the function that provides the data.

router = APIRouter() 


@router.get("/deals", response_model=list[DealOut])     # Tells FastAPI if someone visits GET /deals, run list_deals()
def list_deals():
    return get_mock_deals()