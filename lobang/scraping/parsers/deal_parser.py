"""
Purpose: Orchestrate raw Telegram post parsing into a structured deal record.
"""

from datetime import date, datetime
from typing import Optional

from .utils import normalize_text
from ._1_classification import is_food_deal
from ._2_extract_title import extract_title
from ._3_extract_merchant_name import extract_merchant_name
from ._4_extract_date_validity import extract_date_validity
from ._5_extract_location import extract_location_hint
from ._6_extract_place_info import (fetch_place, extract_cuisine, extract_price_level,
                                     extract_address, estimate_outlet_coverage)
from ._7_resolve_location import resolve_location_metadata
from ._8_extract_more_info_url import extract_more_info_url
from ._9_extract_time_validity import extract_time_text


def _get_scrape_date(value: datetime | date | None) -> date:
    """
    Return the scrape date in date form for downstream validity parsing.
    """
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    raise ValueError("parse_raw_post requires scraped_at as a date or datetime")


def _nonempty_lines(text: str) -> list[str]:
    """
    Return stripped, non-blank lines from normalized post text.
    """
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_raw_post(row: dict) -> Optional[dict]:
    """
    Parse one raw post row into the structured deal payload stored in deals.
    """
    text = normalize_text(row.get("raw_text", ""))
    raw_payload = row.get("raw_payload") or {}

    if not text:
        return None

    if not is_food_deal(text):
        return None

    lines = _nonempty_lines(text)
    title = extract_title(lines, text)
    merchant_name = extract_merchant_name(text, title)

    scraped_at = _get_scrape_date(row.get("scraped_at"))
    start_date, end_date = extract_date_validity(text, scraped_at)

    explicit_location = extract_location_hint(text)

    place = fetch_place(merchant_name) if merchant_name else None
    cuisine = extract_cuisine(place)
    price_level = extract_price_level(place)
    address = extract_address(place)

    if merchant_name:
        coverage = estimate_outlet_coverage(merchant_name)
        outlet_count = coverage["outlet_count"]
        covered_regions = coverage["covered_regions"]
    else:
        outlet_count = 0
        covered_regions = []

    location_meta = resolve_location_metadata(text, explicit_location, covered_regions)
    location_text = location_meta["location_text"]
    display_location = location_meta["display_location"]
    location_mode = location_meta["location_mode"]
    covered_regions = location_meta["covered_regions"]

    more_info_url = extract_more_info_url(text)
    image_url = row.get("image_url") or raw_payload.get("image_url")
    time_text = extract_time_text(text)

    return {
        "raw_deal_id": row.get("id"),
        "source_url": row.get("source_url"),
        "content_hash": row.get("content_hash"),
        "more_info_url": more_info_url,
        "image_url": image_url,
        "time_text": time_text,

        "title": title,
        "merchant_name": merchant_name,

        "start_date": start_date,
        "end_date": end_date,

        "cuisine": cuisine,
        "price_level": price_level,
        "address": address,

        "outlet_count": outlet_count,
        "covered_regions": covered_regions,
        "location_text": location_text,
        "display_location": display_location,
        "location_mode": location_mode,
    }
