"""
Purpose: Create, delete, and list a user's bookmarked deals.
"""

from typing import Any
from src.database.connection import get_conn


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
            return [
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
                for row in rows
            ]
    finally:
        conn.close()
