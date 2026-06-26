"""
Purpose: Resolve frontend-facing location display from explicit location text and outlet coverage
"""

from __future__ import annotations

import re
from typing import Optional

from .patterns import (REGION_ORDER, EXPLICIT_LOCATION_PATTERNS)
from .utils import clean_line


def _normalize_regions(covered_regions: list[str] | None) -> list[str]:
    if not covered_regions:
        return []

    seen = set()
    ordered = []

    for region in REGION_ORDER:
        if region in covered_regions and region not in seen:
            seen.add(region)
            ordered.append(region)

    return ordered


def _extract_explicit_availability(raw_text: str) -> Optional[str]:
    if not raw_text:
        return None

    for pattern in EXPLICIT_LOCATION_PATTERNS:
        match = re.search(pattern, raw_text, flags=re.IGNORECASE)
        if match:
            return clean_line(match.group(1))

    return None


def format_covered_regions(covered_regions: list[str] | None) -> Optional[str]:
    regions = _normalize_regions(covered_regions)

    if not regions:
        return None

    if len(regions) == len(REGION_ORDER):
        return "Islandwide"

    return ", ".join(region.title() for region in regions)


def resolve_location_metadata(
    raw_text: str,
    explicit_location: Optional[str],
    covered_regions: list[str] | None,
) -> dict:
    """
    Priority:
        1. explicit location
        2. explicit availability clause
        3. outlet coverage
        4. hidden
    """
    explicit_location = clean_line(explicit_location) if explicit_location else None
    regions = _normalize_regions(covered_regions)

    availability_clause = _extract_explicit_availability(raw_text)
    if explicit_location:
        return {
            "location_text": explicit_location,
            "display_location": explicit_location,
            "location_mode": "explicit",
            "covered_regions": regions,
        }

    if availability_clause:
        return {
            "location_text": availability_clause,
            "display_location": availability_clause,
            "location_mode": "explicit",
            "covered_regions": regions,
        }

    display_location = format_covered_regions(regions)

    if display_location == "Islandwide":
        location_mode = "islandwide"
    elif display_location:
        location_mode = "coverage"
    else:
        location_mode = "hidden"

    return {
        "location_text": None,
        "display_location": display_location,
        "location_mode": location_mode,
        "covered_regions": regions,
    }