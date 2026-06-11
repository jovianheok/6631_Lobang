"""
Purpose: Serve as the main parser entry point that orchestrates classification and extraction modules to convert a raw Telegram post into a structured deal record
"""
from typing import Optional

from utils import normalize_text
from _1_classification import is_food_deal
from _2_title import extract_title
from _3_merchant import extract_merchant_name

def parse_raw_post(raw_post: dict) -> Optional[dict]:
    text = normalize_text(raw_post.get("text", ""))
    if not text:
        return None

    if not is_food_deal(text):
        return None

    title = extract_title(lines, text)
    merchant_name = extract_merchant_name(text, title)
    # discount = extract_discount(text)
    # location = extract_location(text)
    # expiry = extract_expiry(text)

    return {
        "title": title,
        "merchant_name": merchant_name,
    }