"""
Purpose: Save raw posts into raw_deals table and parsed deals into deals table
"""

from psycopg2.extras import Json

from .connection import get_conn
from .queries import INSERT_RAW_POST, INSERT_PARSED_DEAL


def save_raw_posts(raw_posts: list[dict], source_id: int):
    """
    Purpose: Save scraped posts into raw_deals table
    """
    inserted_ids = []
    conn = get_conn()

    try:
        with conn:
            with conn.cursor() as cur:
                for post in raw_posts:
                    cur.execute(
                        INSERT_RAW_POST,
                        (
                            source_id,
                            post.get("source_url"),
                            post.get("text"),
                            Json(post),
                            post.get("content_hash"),
                        ),
                    )
                    row = cur.fetchone()
                    if row:
                        inserted_ids.append(row[0])
        return inserted_ids
    finally:
        conn.close()


def save_parsed_deals(parsed_deals: list[dict], source_id: int):
    """
    Purpose: Save parsed deals into deals table
    """
    inserted_ids = []
    conn = get_conn()

    try:
        with conn:
            with conn.cursor() as cur:
                for deal in parsed_deals:
                    if not deal:
                        continue

                    cur.execute(
                        INSERT_PARSED_DEAL,
                        (
                            deal.get("raw_deal_id"),
                            source_id,
                            deal.get("source_url"),
                            deal.get("content_hash"),
                            deal.get("more_info_url"),
                            deal.get("image_url"),
                            deal.get("title"),
                            deal.get("merchant_name"),
                            deal.get("expiry_date"),
                            deal.get("display_until"),
                            deal.get("cuisine"),
                            deal.get("price_level"),
                            deal.get("address"),
                            deal.get("outlet_count"),
                            deal.get("covered_regions") or [],
                            deal.get("location_text"),
                            deal.get("display_location"),
                            deal.get("location_mode"),
                            "active",
                        ),
                    )
                    row = cur.fetchone()
                    if row:
                        inserted_ids.append(row[0])

        return inserted_ids
    finally:
        conn.close()
