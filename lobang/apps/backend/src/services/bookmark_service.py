"""
Purpose: Create, delete, and list a user's bookmarked deals.
"""

from typing import Any
from src.database.connection import get_conn
from src.services.vote_service import get_vote_maps


def add_bookmark(user_id: str, deal_id: int) -> None:
    """Save a deal for the user; a repeat bookmark is a no-op."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO public.bookmarks (user_id, deal_id)
                VALUES (%s, %s)
                ON CONFLICT (user_id, deal_id) DO NOTHING;
                """,
                (user_id, deal_id),
            )
            conn.commit()
    finally:
        conn.close()


def remove_bookmark(user_id: str, deal_id: int) -> None:
    """Remove a saved deal; deleting a missing bookmark is a no-op."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM public.bookmarks WHERE user_id = %s AND deal_id = %s;",
                (user_id, deal_id),
            )
            conn.commit()
    finally:
        conn.close()


def get_bookmarked_deals(user_id: str) -> list[dict[str, Any]]:
    """Return the full deal rows the user has bookmarked, newest bookmark first."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    d.id,
                    d.title,
                    d.merchant_name,
                    d.source_url,
                    d.more_info_url,
                    d.image_url,
                    d.time_text,
                    d.start_date,
                    d.end_date,
                    d.cuisine,
                    d.price_level,
                    d.address,
                    d.covered_regions,
                    d.display_location
                FROM public.bookmarks b
                JOIN public.deals d ON d.id = b.deal_id
                WHERE b.user_id = %s
                ORDER BY b.created_at DESC;
                """,
                (user_id,),
            )
            rows = cur.fetchall()
            deal_ids = [row[0] for row in rows]
            vote_counts, user_votes = get_vote_maps(deal_ids, user_id)
            return [
                {
                    **vote_counts.get(
                        row[0],
                        {"upvote_count": 0, "downvote_count": 0, "community_score": 0},
                    ),
                    "id": row[0],
                    "title": row[1],
                    "merchant_name": row[2],
                    "source_url": row[3],
                    "more_info_url": row[4],
                    "image_url": row[5],
                    "time_text": row[6],
                    "start_date": row[7],
                    "end_date": row[8],
                    "cuisine": row[9],
                    "price_level": row[10],
                    "address": row[11],
                    "covered_regions": row[12] or [],
                    "display_location": row[13],
                    "user_vote": user_votes.get(row[0]),
                    # Columns not yet present on public.deals; null until added.
                    "description": None,
                    "location_name": None,
                    "discount_value": None,
                    "discount_unit": None,
                    "distance_km": None,
                    "score": None,
                }
                for row in rows
            ]
    finally:
        conn.close()
