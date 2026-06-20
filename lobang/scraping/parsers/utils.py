"""
Purpose: Hold reusable helper functions for text cleaning, normalization, and pattern matching
"""

import re
from datetime import date
from typing import Optional
from .patterns import MONTHS

def normalize_text(text: str) -> str:
    """
    Purpose: Clean and standardize raw Telegram text before classification and extraction
    """
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)     # Collapse multiple spaces/tabs
    text = re.sub(r"\n{3,}", "\n\n", text)      # Collapse excessive blank lines
    return text.strip()


def clean_line(value: str) -> str:
    """
    Purpose: Clean extracted values such as titles, merchant names, locations, and dates
    """
    value = re.sub(r"\s+", " ", (value or "").strip())      # value = title or "", then remove whitespace, then replace any spaces, tabs, newlines with a single space
    value = value.strip(" -–—:|•·,\t")      # Remove punctuation from both leading and trailing ends
    return value.strip()        # Remove any leading and trailing whitespace


def extract_first_match(text: str, patterns: list[str],) -> Optional[str]:
    """
    Purpose: Return the first regex match found from a list of patterns
    """
    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if match:
            return match.group(0)

    return None


def parse_day_month_from_text(text: str, post_date: date) -> Optional[date]:
    """
    Purpose: Parse a date and normalize it to YYYY-MM-DD
    Year -> Use the post year by default. If the inferred date is earlier than the post date, roll over to next year.
    """
    # Look for a day + month pattern anywhere in the text.
    match = re.search(r"\b(\d{1,2})\s+([A-Za-z]{3,9})\b", text, flags=re.IGNORECASE)
    if not match:
        return None

    day = int(match.group(1))
    month_name = match.group(2).lower()
    month = MONTHS.get(month_name)

    if month is None:
        return None

    try:
        candidate = date(post_date.year, month, day)        # Build the date using the post year first
    except ValueError:
        return None

    if candidate < post_date:       # If the date already passed relative to the post date, assume it refers to the next year.
        try:
            candidate = date(post_date.year + 1, month, day)
        except ValueError:
            return None

    return candidate