"""
Purpose: Extract a promotion's date validity range from the raw post text.
"""

import re
from datetime import date, timedelta

from .patterns import EXPIRY_KEYWORDS
from .utils import parse_day_month_from_text


def extract_date_validity(text: str, post_date: date) -> tuple[date, date]:
    """
    Purpose: Return a start_date and end_date for the deal.

    Defaults:
    - start_date = post_date
    - end_date = post_date + 30 days
    """
    default_start = post_date
    default_end = post_date + timedelta(days=30)

    # First pass: explicit end-date language such as "Now till 11 Jun".
    keyword_end_date = extract_keyword_end_date(text, post_date)
    if keyword_end_date is not None:
        return default_start, keyword_end_date

    # Second pass: explicit date range such as "1 Aug - 31 Aug".
    date_range = extract_explicit_date_range(text, post_date)
    if date_range is not None:
        return date_range

    # Third pass: a single promo date without keyword phrasing.
    single_date = extract_single_promo_date(text, post_date)
    if single_date is not None:
        return default_start, single_date

    return default_start, default_end


def extract_keyword_end_date(text: str, post_date: date) -> date | None:
    """
    Purpose: Extract an end date from explicit expiry phrasing.
    """
    lowered = text.lower()
    for keyword in EXPIRY_KEYWORDS:
        pattern = rf"\b{re.escape(keyword)}\b\s*(.*)"
        match = re.search(pattern, lowered, flags=re.IGNORECASE)

        if not match:
            continue

        tail = match.group(1).strip()
        if not tail:
            continue

        tail = clean_date_tail(tail)
        parsed = parse_day_month_from_text(tail, post_date)
        if parsed:
            return parsed

    return None


def extract_explicit_date_range(text: str, post_date: date) -> tuple[date, date] | None:
    """
    Purpose: Extract a date validity range from one line containing two dates.
    """
    for line in text.splitlines():
        cleaned = clean_date_tail(line)
        matches = list(
            re.finditer(r"\b(\d{1,2})\s+([A-Za-z]{3,9})\b", cleaned, flags=re.IGNORECASE)
        )
        if len(matches) < 2:
            continue

        first = parse_day_month_from_text(matches[0].group(0), post_date)
        second = parse_day_month_from_text(matches[1].group(0), post_date)
        if first and second:
            return first, second

    return None


def clean_date_tail(text: str) -> str:
    """
    Purpose: Remove text that commonly appears after a date.
    """
    return re.split(r"[,(|)]|\|", text, maxsplit=1)[0].strip()


def extract_single_promo_date(text: str, post_date: date) -> date | None:
    """
    Purpose: Extract a single date from the post and treat it as the end date.
    """
    for line in text.splitlines():
        parsed_date = parse_day_month_from_text(line, post_date)
        if parsed_date:
            return parsed_date

    return None
