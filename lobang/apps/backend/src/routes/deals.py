# deals.py
from fastapi import APIRouter
from src.schemas.deal import DealOut
from src.services.deal_service import get_deals

router = APIRouter()

@router.get("/deals", response_model=list[DealOut])
def list_deals():
    return get_deals()