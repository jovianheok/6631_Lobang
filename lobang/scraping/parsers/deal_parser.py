"""
Purpose: Serve as the main parser entry point that orchestrates classification and extraction modules to convert a raw Telegram post into a structured deal record
"""
from typing import Optional
from datetime import datetime, timedelta

from .utils import normalize_text
from ._1_classification import is_food_deal
from ._2_extract_title import extract_title
from ._3_extract_merchant import extract_merchant_name
from ._4_extract_expiry import extract_expiry
from ._7_enrich_googleplaces.enricher import enrich_merchant

def parse_raw_post(row: dict) -> Optional[dict]:
    text = normalize_text(row.get("raw_text", ""))

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
    # location = extract_location(text)

    # 6. Extract price range
    # 7. Enrich merchant via Google Places to get cuisine, price level and location(?)
    place_info = enrich_merchant(merchant_name) or {}


    return {
        "raw_deal_id": row["id"],
        "source_url": row["source_url"],
        "content_hash": row["content_hash"],

        "title": title,
        "merchant_name": merchant_name,
        "expiry_date": expiry_date,
        "display_until": display_until,
        "cuisine": place_info.get("cuisine"),
        "price_level": place_info.get("price_level"),
        "address": place_info.get("address"),
    }
