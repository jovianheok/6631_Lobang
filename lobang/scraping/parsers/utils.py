"""
Purpose: Hold reusable helper functions for text cleaning, normalization, and pattern matching
"""

import re
from typing import Optional

def normalize_text(text: str) -> str:
    """
    Purpose: Clean and standardize raw Telegram text before classification and extraction
    """
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)     # collapse multiple spaces/tabs
    text = re.sub(r"\n{3,}", "\n\n", text)      # collapse excessive blank lines
    return text.strip()


def clean_line(value: str) -> str:
    """
    Purpose: Clean extracted values such as titles, merchant names, locations, and dates
    """
    value = re.sub(r"\s+", " ", (value or "").strip())      # value = title or "", then remove whitespace, then replace any spaces, tabs, newlines with a single space
    value = value.strip(" -–—:|•·,\t")      # remove punctuation from the ends
    return value.strip()        # remove any leading and trailing whitespace


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