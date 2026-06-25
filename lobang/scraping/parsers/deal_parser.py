"""
Purpose: Serve as the main parser entry point that orchestrates classification and extraction modules to convert a raw Telegram post into a structured deal record
"""
from typing import Optional
from datetime import datetime, timedelta

from .utils import normalize_text
from ._1_classification import is_food_deal
from ._2_extract_title import extract_title
from ._3_extract_merchant_name import extract_merchant_name
from ._4_extract_expiry_date import extract_expiry
from ._5_extract_place_info import (fetch_place, extract_cuisine, extract_price_level, extract_address)

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

    # 5. Enrich merchant via Google Places
    place = fetch_place(merchant_name)
    cuisine = extract_cuisine(place)
    price_level = extract_price_level(place)
    address = extract_address(place)


    return {
        "raw_deal_id": row.get("id"),
        "source_url": row.get("source_url"),
        "content_hash": row.get("content_hash"),

        "title": title,
        "merchant_name": merchant_name,
        "expiry_date": expiry_date,
        "display_until": display_until,
        "cuisine": cuisine,
        "price_level": price_level,
        "address": address,
    }
