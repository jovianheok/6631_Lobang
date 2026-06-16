"""
Purpose: Extract and clean a suitable title from a raw Telegram post for downstream classification and extraction
"""

from __future__ import annotations
import re
from utils import clean_line

def clean_title(title: str) -> str:
    title = clean_line(title)
    title = re.sub(r"[\U0001F300-\U0001FAFF\U00002700-\U000027BF]+", "", title)     # Remove emojis
    title = re.sub(r"^\[[^\]]+\]\s*", "", title)        # Remove leading bracketed tags
    return title.strip()


def extract_title(lines: list[str], text: str) -> str:
    """
    Purpose: Extract the most suitable title from a Telegram post
    """
    if lines:       # Clean the first line and use it as title if it is not empty
        first = clean_title(lines[0])
        if first:
            return first if len(first) <= 120 else first[:120].rstrip()

    fallback = clean_line((text or "").split("\n", 1)[0])       # Otherwise use the first line of the raw text
    return fallback if len(fallback) <= 120 else fallback[:120].rstrip()