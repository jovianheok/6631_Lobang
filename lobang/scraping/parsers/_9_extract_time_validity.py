"""
Purpose: Extract time-of-day windows and recurring validity notes from raw posts.
"""

import re
from typing import Optional

from .patterns import TIME_LINE_PATTERNS
from .utils import clean_line


def extract_time_text(text: str) -> Optional[str]:
    """
    Purpose: Extract the main time-of-day window for the deal, if present.
    """
    if not text:
        return None

    for line in text.splitlines():
        cleaned = clean_line(line)
        if not cleaned:
            continue

        for pattern in TIME_LINE_PATTERNS:
            match = re.search(pattern, cleaned, flags=re.IGNORECASE)
            if not match:
                continue

            if match.lastindex:
                extracted = clean_line(match.group(1))
                return extracted or None
            return None

    return None
