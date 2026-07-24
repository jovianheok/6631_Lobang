"""
Shared pytest fixtures for the scraping suite.
"""

import pytest

from parsers import _6_extract_place_info


@pytest.fixture(autouse=True)
def offline_places(monkeypatch):
    """
    Keep the parser pipeline offline and deterministic. PLACES_API_KEY is read
    once at import (from a local .env, if present), which otherwise makes the
    full-pipeline `parse_raw_post` tests hit the live Google Places API — slow
    (~90s) and flaky. Force it None so fetch_place / estimate_outlet_coverage
    short-circuit. Tests that exercise fetch_place patch a fake key back
    themselves (see test_5_cuisine_price_location).
    """
    monkeypatch.setattr(_6_extract_place_info, "PLACES_API_KEY", None)
