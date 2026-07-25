"""
Purpose: Build consistent frontend-facing deal payloads from database rows.
"""

from typing import Any


DEFAULT_VOTE_DATA = {
    "upvote_count": 0,
    "downvote_count": 0,
    "community_score": 0,
}


def build_deal_payload(
    row: tuple[Any, ...],
    vote_counts: dict[int, dict[str, int]] | None = None,
    user_votes: dict[int, int] | None = None,
    score: float | None = None,
) -> dict[str, Any]:
    """
    Convert a database row into the API payload shape expected by the frontend.
    """
    deal_id = row[0]
    vote_data = (vote_counts or {}).get(deal_id, DEFAULT_VOTE_DATA)
    stored_image_url = row[5]
    raw_post_url = row[14] if len(row) > 14 else None
    image_url = (
        f"/api/v1/deals/{deal_id}/image"
        if stored_image_url or raw_post_url
        else None
    )

    return {
        "id": deal_id,
        "title": row[1],
        "merchant_name": row[2],
        "source_url": row[3],
        "more_info_url": row[4],
        "image_url": image_url,
        "time_text": row[6],
        "start_date": row[7],
        "end_date": row[8],
        "cuisine": row[9],
        "price_level": row[10],
        "address": row[11],
        "covered_regions": row[12] or [],
        "display_location": row[13],
        "upvote_count": vote_data["upvote_count"],
        "downvote_count": vote_data["downvote_count"],
        "community_score": vote_data["community_score"],
        "user_vote": (user_votes or {}).get(deal_id),
        "description": None,
        "location_name": None,
        "discount_value": None,
        "discount_unit": None,
        "distance_km": None,
        "score": score,
    }
