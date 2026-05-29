"""
Pydantic schema definitions for deal-related API responses.
"""

# Base class for creating data validation schemas
from pydantic import BaseModel

# Optional type allows values to be None/null
from typing import Optional

class DealOut(BaseModel):
    """
    Response schema for a deal object.

    Used by FastAPI to:
    - validate API responses
    - serialize Python objects into JSON
    - generate API documentation automatically
    """

    # Unique identifier for the deal
    id: int

    # Main deal title
    title: str

    # Merchant/store name
    # Optional means value can be None
    merchant_name: Optional[str] = None

    # Short deal description
    description: Optional[str] = None

    # Location of the deal
    location_name: Optional[str] = None

    # Discount amount/value
    # Example: 20
    discount_value: Optional[float] = None

    # Discount unit
    # Example: "%", "$"
    discount_unit: Optional[str] = None

    # Original source URL for the deal
    source_url: Optional[str] = None

    # Distance from user in kilometers
    distance_km: Optional[float] = None

    # Ranking/relevance score
    score: Optional[float] = None