"""
Purpose: Determine whether a Telegram post should be classified as a food deal by scoring food, deal, and negative signals
"""

import re
from patterns import (
    FOOD_PATTERNS,
    DEAL_PATTERNS,
    NEGATIVE_PATTERNS,
)

def is_food_deal(text:str) -> bool:
    """
    Purpose: Determine whether a Telegram post should be accepted as a valid food deal based on its food, deal, and negative signals
    """
    food_score = count_pattern_hits(text, FOOD_PATTERNS)
    deal_score = count_pattern_hits(text, DEAL_PATTERNS)
    negative_score = count_pattern_hits(text, NEGATIVE_PATTERNS)

    return (
        food_score >= 1
        and deal_score >= 1
        and negative_score == 0
    )


def count_pattern_hits(text: str, patterns: list[str]) -> int:
    """
    Purpose: Count how many patterns from a pattern list appear in the text
    """
    return sum(
        1
        for pattern in patterns
        if re.search(pattern, text, flags=re.IGNORECASE)
    )

def contains_food_signal(text: str) -> bool:
    """
    Return True if the post contains at least one food signal
    """
    return count_pattern_hits(text, FOOD_PATTERNS) >= 1


def contains_deal_signal(text: str) -> bool:
    """
    Return True if the post contains at least one deal signal
    """
    return count_pattern_hits(text, DEAL_PATTERNS) >= 1

def contains_negative_signal(text: str) -> bool:
    """
    Return True if the post contains at least one negative signal
    """
    return count_pattern_hits(text, NEGATIVE_PATTERNS) >= 1