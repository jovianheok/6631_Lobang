"""
Purpose: Query Google Places API to retrieve cuisine, price level, and address for a given merchant
"""

import os
import requests
from dotenv import load_dotenv
from typing import Optional

from .patterns import CUISINE_TYPE_MAP, PRICE_LEVEL_MAP

# Load environment variables from .env
load_dotenv()

# Read API credentials and endpoint
PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
PLACES_URL = "https://places.googleapis.com/v1/places:searchText"


def fetch_place(merchant_name: str) -> Optional[dict]:
    """
    Purpose: Search Google Places and return the top matching place
    """

    # Cannot call the API without an API key
    if not PLACES_API_KEY:
        print("Missing GOOGLE_PLACES_API_KEY in .env")
        return None

    # Ignore empty merchant names
    if not merchant_name:
        return None

    # Authentication and fields to retrieve
    headers = {
        "X-Goog-Api-Key": PLACES_API_KEY,
        "X-Goog-FieldMask": (
            "places.types,"
            "places.priceLevel,"
            "places.formattedAddress"
        ),
    }

    # Search query biased towards Singapore
    body = {
        "textQuery": f"{merchant_name} Singapore",
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": 1.3521,
                    "longitude": 103.8198,
                },
                "radius": 50000.0,  # Covers all of Singapore
            }
        },
    }

    try:
        # Send POST request to Google Places API
        response = requests.post(
            PLACES_URL,
            json=body,
            headers=headers,
            timeout=5,
        )

        # Raise an exception if the request failed
        response.raise_for_status()

        # Parse JSON response
        data = response.json()

        # Return the top search result
        places = data.get("places", [])
        return places[0] if places else None

    except requests.RequestException as e:
        print(f"Places API error for '{merchant_name}': {e}")
        return None


def extract_cuisine(place: Optional[dict]) -> Optional[str]:
    """
    Purpose: Return the first recognised cuisine from Google's place types
    """
    if not place:
        return None

    for place_type in place.get("types", []):
        if place_type in CUISINE_TYPE_MAP:
            return CUISINE_TYPE_MAP[place_type]

    return None


def extract_price_level(place: Optional[dict]) -> Optional[str]:
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