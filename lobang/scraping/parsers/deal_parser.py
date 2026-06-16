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

    # 1. Check if it is a food deal
    if not is_food_deal(text):
        return None
    
    # Remove surrounding whitespace from each line in text and discard blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # 2. Extract title
    title = extract_title(lines, text)

    # 3. Extract merchant name
    merchant_name = extract_merchant_name(text, title)

    # 4. Extract discount info
    # discount = extract_discount(text)

    # 5. Extract location
    # location = extract_location(text)

    # 6. Extract price range
    # 7. Extract cuisine
    # 8. Extract expiry
    # expiry = extract_expiry(text)


    return {
        "title": title,
        "merchant_name": merchant_name,
    }