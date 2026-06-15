"""
Purpose: Extract, clean, and validate merchant names from Telegram posts using deterministic extraction rules
"""

import re
from typing import Optional

from patterns import MERCHANT_STOPWORDS
from utils import clean_line

def extract_merchant_name(text: str, title: str) -> Optional[str]:
    """
    Purpose: Extract the most likely merchant name from a Telegram post
    """
    candidate = extract_title_prefix(title)
    if not candidate:
        return None

    candidate = clean_merchant_candidate(candidate)
    if not candidate:
        return None

    if is_generic_merchant(candidate):
        return None

    return candidate


def extract_title_prefix(title: str) -> Optional[str]:
    """
    Purpose: Extract the text before ":" or "-" from a title
    """
    match = re.match(r"^([^:|-]+)", title)
    if match:
        return match.group(1).strip()       # the only capturing group consumes character until it hits one of those separators
    return None


def clean_merchant_candidate(value: str) -> str:
    """
    Purpose: Clean a potential merchant name by removing formatting noise and promotional words
    """
    value = clean_line(value)
    value = re.sub(r"\b(" + "|".join(MERCHANT_STOPWORDS) + r")\b", "", value, flags=re.IGNORECASE)      # Remove promotional words
    value = re.sub(r"\s{2,}", " ", value)       # Remove extra spaces

    return value.strip()


def is_generic_merchant(value: str) -> bool:
    """
    Purpose: Determine whether an extracted merchant candidate is too generic to be a valid business name
    """
    if not value:
        return True
    return value.lower() in {word.lower() for word in MERCHANT_STOPWORDS}
