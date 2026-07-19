"""
Purpose: Describe what a deal object should look like when returned to the client
"""

from pydantic import BaseModel      # to create data validation schemas
from typing import Optional     # Optional type allows values to be None/null

class DealOut(BaseModel):
    id: int
    title: str
    merchant_name: Optional[str] = None
    source_url: Optional[str] = None
    more_info_url: Optional[str] = None
    image_url: Optional[str] = None
    time_text: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    upvote_count: int = 0
    downvote_count: int = 0
    community_score: int = 0
    user_vote: Optional[int] = None

    # Enrichment fields (see deals table / Google Places pipeline)
    cuisine: Optional[str] = None
    price_level: Optional[int] = None          # 0..4
    address: Optional[str] = None
    covered_regions: list[str] = []            # SG regions the merchant covers
    display_location: Optional[str] = None     # frontend-friendly location label

    # Not (yet) stored on deals; kept optional so existing UI keeps working
    description: Optional[str] = None
    location_name: Optional[str] = None
    discount_value: Optional[float] = None
    discount_unit: Optional[str] = None
    distance_km: Optional[float] = None
    score: Optional[float] = None
