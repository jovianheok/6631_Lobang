"""
Purpose: Extract, clean, and validate merchant names from Telegram posts using deterministic extraction rules
"""

import re
from typing import Optional

from .patterns import GENERIC_PROMO_WORDS, AT_PATTERNS, NON_MERCHANT_LOCATION_PHRASES
from .utils import clean_line

def extract_merchant_name(text: str, title: str) -> Optional[str]:
    """
    Purpose: Extract the most likely merchant name from a Telegram post
    """
    # 1) Strongest signal: Merchant: Deal
    candidate = extract_merchant_from_title_prefix(title)
    if candidate:
        return candidate

    # 2) Fallback: title contains "at Merchant"
    candidate = extract_merchant_from_at_pattern(title)
    if candidate:
        return candidate

    # 3) Fallback: body contains "at Merchant"
    candidate = extract_merchant_from_at_pattern(text)
    if candidate:
        return candidate

    return None


def extract_merchant_from_title_prefix(title: str) -> Optional[str]:
    """
    Purpose: Attempt to extract the merchant name before ":" from a title
    """
    if ":" not in title:
        return None

    candidate = title.split(":", 1)[0].strip()
    return validate_merchant_candidate(candidate)


def extract_merchant_from_at_pattern(content: str) -> Optional[str]:
    """
    Purpose: Attempt to extract merchant name after 'at'
    """
    for pattern in AT_PATTERNS:
        match = re.search(pattern, content, flags=re.IGNORECASE)
        if not match:
            continue

        candidate = validate_merchant_candidate(match.group(1))
        if candidate:
            return candidate

    return None


def validate_merchant_candidate(candidate: Optional[str]) -> Optional[str]:
    """
    Purpose: Validate and clean a potential merchant name, rejecting generic or invalid candidates.
    """
    if not candidate:
        return None

    candidate = clean_line(candidate)

    if not candidate:
        return None

    # Reject generic promo words
    if candidate.lower() in {word.lower() for word in GENERIC_PROMO_WORDS}:
        return None

    # Reject common non-merchant location phrases
    if candidate.lower() in NON_MERCHANT_LOCATION_PHRASES:
        return None

    # Reject pure numbers
    if candidate.isdigit():
        return None

    # Reject obvious dates/times accidentally captured
    if re.fullmatch(r"\d{1,2}(:\d{2})?\s*(am|pm)", candidate, flags=re.IGNORECASE):
        return None

    return candidate
    

