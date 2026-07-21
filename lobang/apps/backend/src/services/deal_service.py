"""
Purpose: Query the database and prepare data
"""

from typing import Any      # type hints for better readability and autocomplete support
from dotenv import load_dotenv
from src.database.connection import get_conn
from src.services.deal_payloads import build_deal_payload, DEFAULT_VOTE_DATA
from src.services.preference_service import get_or_create_preferences
from src.services.vote_service import get_vote_maps

load_dotenv()

def get_deals(user_id: str | None = None) -> list[dict[str, Any]]:
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
                    more_info_url,
                    image_url,
                    time_text,
                    start_date,
                    end_date,
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

            deal_ids = [row[0] for row in rows]
            vote_counts, user_votes = get_vote_maps(deal_ids, user_id)

            return [
                build_deal_payload(row, vote_counts=vote_counts, user_votes=user_votes)
                for row in rows
            ]

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
                    more_info_url,
                    image_url,
                    time_text,
                    start_date,
                    end_date,
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

    deal_ids = [row[0] for row in rows]
    vote_counts, user_votes = get_vote_maps(deal_ids, user_id)

    deals: list[dict[str, Any]] = []

    for row in rows:
        price_level = row[10]
        covered_regions = row[12] or []
        vote_data = vote_counts.get(row[0], DEFAULT_VOTE_DATA)

        # Hard price filter, only when both sides are known.
        if max_price is not None and price_level is not None and price_level > max_price:
            continue

        score = 0.0
        if pref_cuisines and row[9] in pref_cuisines:
            score += 2.0
        if pref_regions and any(region in pref_regions for region in covered_regions):
            score += 2.0
        if max_price is not None and price_level is not None and price_level <= max_price:
            score += 1.0
        total_votes = vote_data["upvote_count"] + vote_data["downvote_count"]
        if total_votes >= 5:
            score += max(min(vote_data["community_score"], 3), -3) * 0.25

        deals.append(
            build_deal_payload(
                row,
                vote_counts=vote_counts,
                user_votes=user_votes,
                score=score,
            )
        )

    # Stable sort keeps the created_at DESC ordering within equal scores.
    deals.sort(key=lambda deal: deal["score"], reverse=True)

    return deals
