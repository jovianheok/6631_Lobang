"""
Purpose: Resolve frontend-facing location display from explicit location text
and outlet coverage.

This module should only decide what the frontend sees.
It should not:
- extract explicit location text from raw Telegram posts
- call Google Places
- infer business meaning beyond display rules
"""

from __future__ import annotations

from typing import Optional

from .patterns import REGION_ORDER
from .utils import clean_line


def _normalize_regions(covered_regions: list[str] | None) -> list[str]:
    """
    Return unique regions in canonical REGION_ORDER.
    """
    if not covered_regions:
        return []

    seen = set()
    ordered: list[str] = []

    for region in REGION_ORDER:
        if region in covered_regions and region not in seen:
            seen.add(region)
            ordered.append(region)

    return ordered


def format_covered_regions(covered_regions: list[str] | None) -> Optional[str]:
    """
    Convert a region list into frontend-friendly display text.

    If all five regions are covered, return "Islandwide".
    Otherwise return a comma-separated list like:
        "north, east, central"
    """
    regions = _normalize_regions(covered_regions)

    if not regions:
        return None

    if len(regions) == len(REGION_ORDER):
        return "Islandwide"

    return ", ".join(region.title() for region in regions)


def resolve_location_metadata(
    explicit_location: Optional[str],
    covered_regions: list[str] | None,
) -> dict:
    """
    Decide what the frontend should display.

    Priority:
      1. explicit location in raw text
      2. covered regions from outlet inference
      3. nothing
    """
    explicit_location = clean_line(explicit_location) if explicit_location else None
    regions = _normalize_regions(covered_regions)
    display_location = None
    location_mode = "hidden"

    if explicit_location:
        display_location = explicit_location
        location_mode = "explicit"
    else:
        display_location = format_covered_regions(regions)
        if display_location == "Islandwide":
            location_mode = "islandwide"
        elif display_location:
            location_mode = "coverage"

    return {
        "location_text": explicit_location,
        "display_location": display_location,
        "location_mode": location_mode,
        "covered_regions": regions,
    }