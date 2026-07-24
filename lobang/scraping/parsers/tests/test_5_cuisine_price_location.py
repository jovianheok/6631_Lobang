"""
Tests for the Google Places enrichment helpers in parsers/_6_extract_place_info.

The pure extractors (extract_cuisine / extract_price_level / extract_address)
take a Google Places `place` dict and need no mocking. fetch_place performs the
network call, so we patch the module-level SESSION and PLACES_API_KEY instead of
hitting the real API.
"""

from unittest.mock import patch, MagicMock

from parsers import _6_extract_place_info as place_info
from parsers._6_extract_place_info import (
    extract_cuisine,
    extract_price_level,
    extract_address,
    fetch_place,
)


# --- extract_cuisine (pure) ---

def test_extract_cuisine_known_type():
    place = {"types": ["chinese_restaurant", "restaurant"]}
    assert extract_cuisine(place) == "Chinese"


def test_extract_cuisine_returns_first_recognised_match():
    # "restaurant" isn't in CUISINE_TYPE_MAP; "cafe" is the first that maps.
    place = {"types": ["restaurant", "cafe", "bakery"]}
    assert extract_cuisine(place) == "Cafe"


def test_extract_cuisine_unknown_type():
    assert extract_cuisine({"types": ["point_of_interest"]}) is None


def test_extract_cuisine_no_types():
    assert extract_cuisine({}) is None


def test_extract_cuisine_none_place():
    assert extract_cuisine(None) is None


# --- extract_price_level (pure) ---

def test_extract_price_level_maps_google_label():
    assert extract_price_level({"priceLevel": "PRICE_LEVEL_MODERATE"}) == 2


def test_extract_price_level_unknown_label():
    assert extract_price_level({"priceLevel": "PRICE_LEVEL_UNSPECIFIED"}) is None


def test_extract_price_level_none_place():
    assert extract_price_level(None) is None


# --- extract_address (pure) ---

def test_extract_address_present():
    place = {"formattedAddress": "123 Orchard Rd, Singapore 238858"}
    assert extract_address(place) == "123 Orchard Rd, Singapore 238858"


def test_extract_address_missing():
    assert extract_address({}) is None


def test_extract_address_none_place():
    assert extract_address(None) is None


# --- fetch_place (network mocked) ---

def _mock_response(places: list) -> MagicMock:
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"places": places}
    return response


@patch.object(place_info, "PLACES_API_KEY", "fake-key")
@patch.object(place_info.SESSION, "post")
def test_fetch_place_returns_top_match(mock_post):
    top = {
        "types": ["hamburger_restaurant"],
        "priceLevel": "PRICE_LEVEL_MODERATE",
        "formattedAddress": "123 Orchard Rd, Singapore 238858",
    }
    mock_post.return_value = _mock_response([top, {"types": ["restaurant"]}])

    assert fetch_place("Burger King") == top


@patch.object(place_info, "PLACES_API_KEY", "fake-key")
@patch.object(place_info.SESSION, "post")
def test_fetch_place_no_results(mock_post):
    mock_post.return_value = _mock_response([])
    assert fetch_place("Unknown Place XYZ") is None


@patch.object(place_info, "PLACES_API_KEY", None)
def test_fetch_place_missing_api_key():
    # No key → short-circuits before any network call.
    assert fetch_place("Starbucks") is None


@patch.object(place_info, "PLACES_API_KEY", "fake-key")
def test_fetch_place_empty_name():
    assert fetch_place("") is None


@patch.object(place_info, "PLACES_API_KEY", "fake-key")
@patch.object(place_info.SESSION, "post")
def test_fetch_place_api_error_returns_none(mock_post):
    import requests

    mock_post.side_effect = requests.RequestException("Connection timeout")
    assert fetch_place("Starbucks") is None
