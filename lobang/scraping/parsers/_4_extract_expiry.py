"""
Purpose: Extract the promotion expiry date from the text in raw posts
"""

import re
from datetime import date
from typing import Optional

from .patterns import EXPIRY_KEYWORDS


def extract_expiry(text: str, post_date: date) -> Optional[str]:
    """
    Purpose: Extract the promotion expiry date
    """
     # First pass: explicit expiry language anywhere in the post
    keyword_date = extract_keyword_expiry(text, post_date)
    if keyword_date is not None:
        return keyword_date

    # Second pass: look at calendar lines for one-day promotions
    single_date = extract_single_promo_date(text, post_date)
    if single_date is not None:
        return single_date

    return None

def extract_keyword_expiry(text, post_date):
    lowered = text.lower()

    # Check each keyword and try to parse the date that follows it.
    for keyword in EXPIRY_KEYWORDS:
        # Match the keyword and capture the text after it.
        # Example:
        #   "Now till 30 Jun" -> captures "30 Jun"
        pattern = rf"\b{re.escape(keyword)}\b\s*(.*)"
        match = re.search(pattern, lowered, flags=re.IGNORECASE)

        if not match:
            continue

        tail = match.group(1).strip()
        if not tail:
            continue

        # Remove trailing noise such as time, punctuation, or brackets.
        tail = clean_date_tail(tail)

        parsed = parse_day_month_from_text(tail, post_date)
        if parsed is not None:
            return parsed

        if keyword == "limited time only":      # If the keyword itself is "limited time only", there may be no explicit date.
            return None

    return None
    
def extract_single_promo_date(text, post_date):
    pass