"""
Purpose: Orchestrate raw Telegram post parsing into a structured deal record.
"""

from typing import Optional
from datetime import datetime, timedelta

from .utils import normalize_text
from ._1_classification import is_food_deal
from ._2_extract_title import extract_title
from ._3_extract_merchant_name import extract_merchant_name
from ._4_extract_expiry_date import extract_expiry
from ._5_extract_location import extract_location_hint
from ._6_extract_place_info import (fetch_place, extract_cuisine, extract_price_level,
                                     extract_address, estimate_outlet_coverage)
from ._7_resolve_location import resolve_location_metadata
from ._8_extract_more_info_url import extract_more_info_url

def parse_raw_post(row: dict) -> Optional[dict]:
    text = normalize_text(row.get("raw_text", ""))
    raw_payload = row.get("raw_payload") or {}

    if not text:
        return None

    # 1. Check if it is a food deal
    if not is_food_deal(text):
        return None
    
    # Remove surrounding whitespace from each line in text and discard blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # 2. Extract title
    title = extract_title(lines, text)

    # 3. Extract merchant name
    merchant_name = extract_merchant_name(text, title)

    # 4. Extract expiry
    scraped_at = row.get("scraped_at", "").date()
    expiry_date = extract_expiry(text, scraped_at)
    display_until = (expiry_date if expiry_date is not None else scraped_at + timedelta(days=30))

    # 5. Extract location
    explicit_location = extract_location_hint(text)

    # 6. Enrich cuisine, price_level, address via Google Places
    place = fetch_place(merchant_name) if merchant_name else None

    cuisine = extract_cuisine(place)
    price_level = extract_price_level(place)
    address = extract_address(place)

    # 6. Estimate outlet coverage for restaurant chain
    if merchant_name:
        coverage = estimate_outlet_coverage(merchant_name)
        outlet_count = coverage["outlet_count"]
        covered_regions = coverage["covered_regions"]
    else:
        outlet_count = 0
        covered_regions = []

    # 7. Resolve frontend-facing location display
    location_meta = resolve_location_metadata(text, explicit_location, covered_regions)

    location_text = location_meta["location_text"]
    display_location = location_meta["display_location"]
    location_mode = location_meta["location_mode"]
    covered_regions = location_meta["covered_regions"]

    # 8. Extract more_info_url
    more_info_url = extract_more_info_url(text)
    image_url = row.get("image_url") or raw_payload.get("image_url")


    return {
        "raw_deal_id": row.get("id"),
        "source_url": row.get("source_url"),
        "content_hash": row.get("content_hash"),
        "more_info_url": more_info_url,
        "image_url": image_url,

        "title": title,
        "merchant_name": merchant_name,

        "expiry_date": expiry_date,
        "display_until": display_until,

        "cuisine": cuisine,
        "price_level": price_level,
        "address": address,

        "outlet_count": outlet_count,
        "covered_regions": covered_regions,
        "location_text": location_text,
        "display_location": display_location,
        "location_mode": location_mode,
    }
