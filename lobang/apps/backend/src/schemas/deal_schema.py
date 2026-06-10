"""
Purpose: Describe what a deal object should look like when returned to the client
"""

from pydantic import BaseModel      # to create data validation schemas
from typing import Optional     # Optional type allows values to be None/null

class DealOut(BaseModel):
    id: int
    title: str
    merchant_name: Optional[str] = None
    description: Optional[str] = None
    location_name: Optional[str] = None
    discount_value: Optional[float] = None
    discount_unit: Optional[str] = None
    source_url: Optional[str] = None
    distance_km: Optional[float] = None
    score: Optional[float] = None