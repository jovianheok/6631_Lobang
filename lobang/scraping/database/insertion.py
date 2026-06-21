"""
Purpose: Save raw posts into raw_deals table and parsed deals into deals table in Supabase
"""

from psycopg2.extras import Json        # to convert Python dictionaries into PostgreSQL JSON format

from .connection import get_conn
from .queries import (INSERT_RAW_POST, INSERT_PARSED_DEAL,)

# Save scraped posts into database
def save_raw_posts(raw_posts: list[dict], source_id: int):
    """
    Purpose: Save raw posts into raw_deals table
    """
    inserted_ids = []       # to store database ID of each post for counting purpose
    conn = get_conn()

    try:
        with conn:
            with conn.cursor() as cur:      # Create a cursor to run SQL commands
                for post in raw_posts:
                    cur.execute(INSERT_RAW_POST,
                                (source_id,                 # source_id
                                post["source_url"],         # source_url
                                post["text"],               # raw_text
                                Json(post),                 # raw_payload in a dictionary
                                post["content_hash"],       # content_hash
                                ),
                    )         
                    row = cur.fetchone()        # Fetch the returned row
                    if row:
                        inserted_ids.append(row[0]) # Get the row id and insert into inserted_ids
        return inserted_ids
    
    finally:
        conn.close()


def save_parsed_deals(parsed_deals: list[dict], source_id: int):
    """
    Purpose: Save parsed deals into deals table in Supabase
    """
    inserted_ids = []
    conn = get_conn()

    try:
        with conn:
            with conn.cursor() as cur:
                for deal in parsed_deals:

                    cur.execute(INSERT_PARSED_DEAL,
                                (deal.get("raw_deal_id"),       # raw_deal_id
                                 source_id,                     # source_id
                                 deal.get("source_url"),        # source_url
                                 deal.get("content_hash"),      # content_hash

                                 deal.get("title"),             # title
                                 deal.get("merchant_name"),     # merchant_name
                                 deal.get("expiry_date"),       # expiry
                                 deal.get("display_until"),     # display_until

                                "active",                       # status
                                 ),
                    )
                    row = cur.fetchone()
                    if row:
                        inserted_ids.append(row[0])

        return inserted_ids
    
    finally:
        conn.close()

