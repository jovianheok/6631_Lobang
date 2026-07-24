"""
Purpose: Extract a frontend-safe "more info" URL from the raw Telegram post text.
"""

import re
from typing import Optional

from .patterns import MORE_INFO_PATTERNS


def extract_more_info_url(text: str) -> Optional[str]:
    """
    Purpose: Extract a URL from "More info" / "Find out more" style lines.
    """
    if not text:
        return None

    for pattern in MORE_INFO_PATTERNS:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue

        url = match.group(1).strip().rstrip(".,;)")
        if url.startswith("http://") or url.startswith("https://"):
            return url
        return f"https://{url}"

    return None
