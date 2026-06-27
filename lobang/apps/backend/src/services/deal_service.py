"""
Purpose: Query the database and prepare data
"""

import os
from typing import Any      # type hints for better readability and autocomplete support
import psycopg2
from dotenv import load_dotenv
from src.database.connection import get_conn
from src.services.preference_service import get_or_create_preferences

load_dotenv()

def get_deals() -> list[dict[str, Any]]:
    """
    Purpose: Retrieve deal data from the database and convert to Python objects
    """
    conn = get_conn()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    title,
                    merchant_name,
                    source_url,
                    cuisine,
                    price_level,
                    address,
                    covered_regions,
                    display_location
                FROM public.deals
                WHERE status = 'active'
                ORDER BY created_at DESC
                LIMIT 50;
                """
            )

            rows = cur.fetchall()       # Fetch all query results

            deals: list[dict[str, Any]] = []        # Store processed deals as a list of dictionaries

            for row in rows:
                deals.append(       # Convert each database row into a dictionary
                    {
                        "id": row[0],
                        "title": row[1],
                        "merchant_name": row[2],
                        "source_url": row[3],
                        "cuisine": row[4],
                        "price_level": row[5],
                        "address": row[6],
                        "covered_regions": row[7] or [],
                        "display_location": row[8],
                    }
                )

            return deals

    finally:
        conn.close()


def get_for_you_deals(user_id: str) -> list[dict[str, Any]]:
    """
    Purpose: Curate active deals for a user based on their saved preferences.

    Price acts as a hard filter, but only when both the user's max price and the
    deal's price are known (so deals still missing enrichment aren't dropped).
    Cuisine and region matches are soft ranking signals: deals are returned
    highest-match first, with newer deals breaking ties.
    """
    prefs = get_or_create_preferences(user_id)
    pref_cuisines = set(prefs.get("cuisine_preferences") or [])
    pref_regions = set(prefs.get("preferred_regions") or [])
    max_price = prefs.get("max_price_level")

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    title,
                    merchant_name,
                    source_url,
                    cuisine,
                    price_level,
                    address,
                    covered_regions,
                    display_location
                FROM public.deals
                WHERE status = 'active'
                ORDER BY created_at DESC;
                """
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    deals: list[dict[str, Any]] = []

    for row in rows:
        price_level = row[5]
        covered_regions = row[7] or []

        # Hard price filter, only when both sides are known.
        if max_price is not None and price_level is not None and price_level > max_price:
            continue

        score = 0.0
        if pref_cuisines and row[4] in pref_cuisines:
            score += 2.0
        if pref_regions and any(region in pref_regions for region in covered_regions):
            score += 2.0
        if max_price is not None and price_level is not None and price_level <= max_price:
            score += 1.0

        deals.append(
            {
                "id": row[0],
                "title": row[1],
                "merchant_name": row[2],
                "source_url": row[3],
                "cuisine": row[4],
                "price_level": price_level,
                "address": row[6],
                "covered_regions": covered_regions,
                "display_location": row[8],
                "score": score,
            }
        )

    # Stable sort keeps the created_at DESC ordering within equal scores.
    deals.sort(key=lambda deal: deal["score"], reverse=True)

    return deals