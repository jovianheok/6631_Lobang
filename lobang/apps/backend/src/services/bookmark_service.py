"""
Purpose: Create, delete, and list a user's bookmarked deals.
"""

from typing import Any
from src.database.connection import get_conn
from src.services.deal_payloads import build_deal_payload
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
                    COALESCE(d.image_url, rd.raw_payload->>'image_url') AS image_url,
                    d.time_text,
                    d.start_date,
                    d.end_date,
                    d.cuisine,
                    d.price_level,
                    d.address,
                    d.covered_regions,
                    d.display_location,
                    rd.raw_payload->>'post_url' AS raw_post_url
                FROM public.bookmarks b
                JOIN public.deals d ON d.id = b.deal_id
                LEFT JOIN public.raw_deals rd ON rd.id = d.raw_deal_id
                WHERE b.user_id = %s
                ORDER BY b.created_at DESC;
                """,
                (user_id,),
            )
            rows = cur.fetchall()
            deal_ids = [row[0] for row in rows]
            vote_counts, user_votes = get_vote_maps(deal_ids, user_id)
            return [
                build_deal_payload(row, vote_counts=vote_counts, user_votes=user_votes)
                for row in rows
            ]
    finally:
        conn.close()
