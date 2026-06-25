"""
Purpose: Extract explicit location hints from raw Telegram deal text
"""

from __future__ import annotations

from typing import Optional

from .patterns import LOCATION_HINT_PATTERNS
from .utils import clean_line, extract_first_group, normalize_text


def extract_location_hint(text: str) -> Optional[str]:
    """
    Purpose: Extract an explicit location hint from raw Telegram text
    """
    if not text:
        return None

    normalized = normalize_text(text)

    # Try line-by-line first so we favor clear explicit location clauses
    lines = [line.strip() for line in normalized.splitlines() if line.strip()]
    candidates = lines + [normalized]

    for candidate in candidates:
        value = extract_first_group(candidate, LOCATION_HINT_PATTERNS)
        if value:
            value = clean_line(value)
            if value:
                return value

    return None