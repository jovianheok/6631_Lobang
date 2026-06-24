import pytest
from unittest.mock import patch, MagicMock
from ...scrapers import enrich_merchant, extract_cuisine


# --- extract_cuisine tests (no mocking needed) ---

def test_extract_cuisine_known_type():
    assert extract_cuisine(["chinese_restaurant", "restaurant"]) == "Chinese"

def test_extract_cuisine_returns_first_match():
    assert extract_cuisine(["cafe", "bakery"]) == "Cafe"

def test_extract_cuisine_unknown_type():
    assert extract_cuisine(["point_of_interest"]) is None

def test_extract_cuisine_empty():
    assert extract_cuisine([]) is None


# --- enrich_merchant tests (mock requests.post) ---

def make_mock_response(places: list) -> MagicMock:
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = {"places": places}
    return mock


@patch("scrapers.googleplaces.enricher.PLACES_API_KEY", "fake-key")
@patch("scrapers.googleplaces.enricher.requests.post")
def test_enrich_merchant_happy_path(mock_post):
    mock_post.return_value = make_mock_response([{
        "types": ["hamburger_restaurant"],
        "priceLevel": "PRICE_LEVEL_MODERATE",
        "formattedAddress": "123 Orchard Rd, Singapore 238858",
    }])

    result = enrich_merchant("Burger King")

    assert result == {
        "cuisine": "Burgers",
        "price_level": 2,
        "address": "123 Orchard Rd, Singapore 238858",
    }


@patch("scrapers.googleplaces.enricher.PLACES_API_KEY", "fake-key")
@patch("scrapers.googleplaces.enricher.requests.post")
def test_enrich_merchant_no_results(mock_post):
    mock_post.return_value = make_mock_response([])

    result = enrich_merchant("Unknown Place XYZ")

    assert result is None


@patch("scrapers.googleplaces.enricher.PLACES_API_KEY", None)
def test_enrich_merchant_missing_api_key():
    result = enrich_merchant("Starbucks")
    assert result is None


@patch("scrapers.googleplaces.enricher.PLACES_API_KEY", "fake-key")
def test_enrich_merchant_empty_name():
    result = enrich_merchant("")
    assert result is None


@patch("scrapers.googleplaces.enricher.PLACES_API_KEY", "fake-key")
@patch("scrapers.googleplaces.enricher.requests.post")
def test_enrich_merchant_api_error(mock_post):
    mock_post.side_effect = Exception("Connection timeout")

    result = enrich_merchant("Starbucks")

    assert result is None
