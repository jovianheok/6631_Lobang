"""
Purpose: Query Google Places to enrich a merchant with cuisine, price level,
address, outlet count, and covered Singapore regions
"""

from __future__ import annotations

import os
import time
from typing import Optional

import requests
from dotenv import load_dotenv

from .patterns import (
    CUISINE_TYPE_MAP,
    PRICE_LEVEL_MAP,
    REGION_ORDER,
    ISLANDWIDE_OUTLET_THRESHOLD,
)
from .utils import infer_region_from_google_place

load_dotenv()

PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
SESSION = requests.Session()


def _search_places(merchant_name: str, page_token: Optional[str] = None) -> dict:
    """
    Perform one Google Places Text Search request for a merchant.
    """
    if not PLACES_API_KEY:
        raise RuntimeError("Missing GOOGLE_PLACES_API_KEY in .env")

    headers = {
        "X-Goog-Api-Key": PLACES_API_KEY,
        "X-Goog-FieldMask": (
            "places.id,"
            "places.displayName,"
            "places.types,"
            "places.priceLevel,"
            "places.formattedAddress,"
            "places.location,"
            "nextPageToken"
        ),
    }

    body = {
        "textQuery": f"{merchant_name} Singapore",
        "locationBias": {
            "circle": {
                "center": {"latitude": 1.3521, "longitude": 103.8198},
                "radius": 50000.0,
            }
        },
    }

    if page_token:
        body["pageToken"] = page_token

    response = SESSION.post(
        PLACES_URL,
        json=body,
        headers=headers,
        timeout=8,
    )
    response.raise_for_status()
    return response.json()


def fetch_place(merchant_name: str) -> Optional[dict]:
    """
    Purpose: Search Google Places and return the top matching place
    """
    if not PLACES_API_KEY:
        print("Missing GOOGLE_PLACES_API_KEY in .env")
        return None

    merchant_name = (merchant_name or "").strip()
    if not merchant_name:
        return None

    try:
        data = _search_places(merchant_name)
        places = data.get("places", [])
        return places[0] if places else None

    except requests.RequestException as e:
        print(f"Places API error for '{merchant_name}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error for '{merchant_name}': {e}")
        return None


def fetch_outlets(merchant_name: str) -> list[dict]:
    """
    Purpose: Retrieve all Google Places results for a merchant in Singapore
    """
    if not PLACES_API_KEY:
        print("Missing GOOGLE_PLACES_API_KEY in .env")
        return []

    merchant_name = (merchant_name or "").strip()
    if not merchant_name:
        return []

    outlets: list[dict] = []
    seen_place_ids: set[str] = set()
    page_token: Optional[str] = None

    try:
        while True:
            data = _search_places(merchant_name, page_token=page_token)
            places = data.get("places", [])

            for place in places:
                place_id = place.get("id")
                if not place_id or place_id in seen_place_ids:
                    continue

                seen_place_ids.add(place_id)
                outlets.append(place)

            page_token = data.get("nextPageToken")
            if not page_token:
                break

            # Google recommends a short pause before reusing the next page token.
            time.sleep(2)

        return outlets

    except requests.RequestException as e:
        print(f"Places API outlet fetch error for '{merchant_name}': {e}")
        return []
    except Exception as e:
        print(f"Unexpected outlet fetch error for '{merchant_name}': {e}")
        return []


def estimate_outlet_coverage(merchant_name: str) -> dict:
    """
    Purpose: Estimate outlet count and covered Singapore regions
    If outlet count is at or above the islandwide threshold, treat as islandwide. Otherwise infer regions from outlet addresses.
    """
    if not PLACES_API_KEY or not merchant_name:
        return {
            "outlet_count": 0,
            "covered_regions": [],
        }

    outlets = fetch_outlets(merchant_name)
    returned_outlet_count = len(outlets)

    if returned_outlet_count >= ISLANDWIDE_OUTLET_THRESHOLD:
        return {
            "outlet_count": returned_outlet_count,
            "covered_regions": REGION_ORDER.copy(),
        }

    seen_regions: set[str] = set()
    for outlet in outlets:
        region = infer_region_from_google_place(outlet)
        if region:
            seen_regions.add(region)

    covered_regions = [region for region in REGION_ORDER if region in seen_regions]

    return {
        "outlet_count": returned_outlet_count,
        "covered_regions": covered_regions,
    }


def extract_cuisine(place: Optional[dict]) -> Optional[str]:
    """
    Purpose: Return the first recognised cuisine from a Google Places types list
    """
    if not place:
        return None

    for place_type in place.get("types", []):
        if place_type in CUISINE_TYPE_MAP:
            return CUISINE_TYPE_MAP[place_type]

    return None


def extract_price_level(place: Optional[dict]) -> Optional[int]:
    """
    Purpose: Convert Google's price level into our internal label
    """
    if not place:
        return None

    return PRICE_LEVEL_MAP.get(place.get("priceLevel"))


def extract_address(place: Optional[dict]) -> Optional[str]:
    """
    Purpose: Return the formatted address
    """
    if not place:
        return None

    return place.get("formattedAddress")