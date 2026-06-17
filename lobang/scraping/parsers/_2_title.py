"""
Purpose: Extract and clean a suitable title from a raw Telegram post for downstream classification and extraction
"""

from __future__ import annotations
import re
from .utils import clean_line

# re.sub(pattern, replacement, string) replaces all matches of pattern in string with replacement

def clean_title(title: str) -> str:
    """
    Purpose: Clean a potential title by removing formatting noise and trailing emojis
    """
    title = clean_line(title)
    title = re.sub(r"[\s\U0001F300-\U0001FAFF\U00002700-\U000027BF]+$", "", title)      # Remove trailing emojis only
    return title.strip()


def extract_title(lines: list[str], text: str) -> str:
    """
    Purpose: Extract the most suitable title from a Telegram post
    """
    if lines:       # Clean the first line and use it as title if it is not empty
        title = clean_title(lines[0])
        if title:
            return title

    first_line = (text or "").split("\n", 1)[0]       # Otherwise use the first line of the raw text
    return clean_title(first_line)