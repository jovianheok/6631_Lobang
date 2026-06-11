"""

"""

import re
from typing import Optional

from patterns import MERCHANT_STOPWORDS
from utils import clean_line

def extract_merchant_name(text: str, fallback_title: str) -> Optional[str]:
    """
    Purpose: Extract the most likely merchant name from a Telegram post
    """

def clean_merchant_candidate(value: str) -> str:
    """
    Purpose: Remove promotional words and clean formatting from a potential merchant name
    """

def is_generic_merchant(value: str) -> bool:
    """
    Purpose: Determine whether an extracted merchant candidate is too generic to be a valid business name
    """
    
def extract_title_prefix(title: str) -> Optional[str]:
    """
    Purpose: Extract the text before ":" or "-" from a title
    """