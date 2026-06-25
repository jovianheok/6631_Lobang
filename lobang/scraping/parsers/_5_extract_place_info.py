"""
Purpose: Given a merchant name, query Google Places API to extract cuisine, price level, and address
"""

import os
import requests
from dotenv import load_dotenv
from typing import Optional
from .patterns import CUISINE_TYPE_MAP, PRICE_LEVEL_MAP

load_dotenv()

PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
PLACES_URL = "https://places.googleapis.com/v1/places:searchText"


def extract_place_info(merchant_name: str) -> Optional[dict]:
    """
    Query Google Places Text Search for a merchant name and return cuisine, price_level, and address.
    Returns None if the API call fails or no results are found.
    """
    if not PLACES_API_KEY:
        print("Missing GOOGLE_PLACES_API_KEY in .env")
        return None

    if not merchant_name:
        return None

    headers = {
        "X-Goog-Api-Key": PLACES_API_KEY,
        "X-Goog-FieldMask": "places.types,places.priceLevel,places.formattedAddress",
    }

    body = {
        "textQuery": f"{merchant_name} Singapore",
        "locationBias": {
            "circle": {
                "center": {"latitude": 1.3521, "longitude": 103.8198},
                "radius": 50000.0,      # 50km radius covers all of Singapore
            }
        },
    }

    try:
        response = requests.post(PLACES_URL, json=body, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        places = data.get("places", [])
        if not places:
            return None

        place = places[0]

        cuisine = extract_cuisine(place.get("types", []))
        price_level = PRICE_LEVEL_MAP.get(place.get("priceLevel"), None)
        address = place.get("formattedAddress")

        return {
            "cuisine": cuisine,
            "price_level": price_level,
            "address": address,
        }

    except Exception as e:
        print(f"Places API error for '{merchant_name}': {e}")
        return None


def extract_cuisine(types: list[str]) -> Optional[str]:
    """
    Return the first recognisable cuisine label from a Google Places types list.
    """
    for t in types:
        if t in CUISINE_TYPE_MAP:
            return CUISINE_TYPE_MAP[t]
    return None
