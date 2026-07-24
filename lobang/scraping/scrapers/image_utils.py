"""
Purpose: Hold pure helper functions for scraper image extraction.
"""

import re


def extract_background_image_url(style: str | None) -> str | None:
    """
    Purpose: Extract the photo URL from Telegram's inline background-image style.
    """
    if not style:
        return None

    match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style)
    if not match:
        return None

    url = match.group(1).strip()
    if not url or url.lower() == "none":
        return None

    return url
