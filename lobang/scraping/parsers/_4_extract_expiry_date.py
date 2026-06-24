"""
Purpose: Extract the promotion expiry date from the text in raw posts
"""

import re
from datetime import date
from typing import Optional

from .patterns import EXPIRY_KEYWORDS
from .utils import parse_day_month_from_text


def extract_expiry(text: str, post_date: date) -> Optional[date]:
    """
    Purpose: Extract the promotion expiry date
    """
     # First pass: explicit expiry language anywhere in the post
    keyword_date = extract_keyword_expiry(text, post_date)
    if keyword_date is not None:
        return keyword_date

    # Second pass: handle posts that have a date but no expiry keywords
    single_date = extract_single_promo_date(text, post_date)
    if single_date is not None:
        return single_date

    return None

def extract_keyword_expiry(text, post_date: date) -> Optional[date]:
    """
    Purpose: Extract expiry date by extracting the date after expiry keyword
    """
    lowered = text.lower()
    for keyword in EXPIRY_KEYWORDS:      # Check each keyword and try to parse the date that follows it
        pattern = rf"\b{re.escape(keyword)}\b\s*(.*)"       # builds a regular expression pattern for the current keyword
                                                            # '.*' matches any character, any number of times
        match = re.search(pattern, lowered, flags=re.IGNORECASE)

        if not match:
            continue

        tail = match.group(1).strip()
        if not tail:
            continue

        tail = clean_date_tail(tail)        # Remove trailing noise such as time, punctuation, or brackets

        parsed = parse_day_month_from_text(tail, post_date)
        if parsed:
            return parsed

    return None
    

def clean_date_tail(text: str) -> str:
    """
    Purpose: Remove text that commonly appears after a date
    """
    return re.split(r"[,(|)]|\|", text, maxsplit=1)[0].strip()


def extract_single_promo_date(text: str, post_date: date) -> Optional[date]:
    """
    Purpose: Extract single day from posts that have no expiry keyword
    """
    for line in text.splitlines():
        parsed_date = parse_day_month_from_text(line, post_date)

        if parsed_date:
            return parsed_date

    return None