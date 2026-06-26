"""
Purpose: Query the database and prepare data
"""

import os
from typing import Any      # type hints for better readability and autocomplete support
import psycopg2
from dotenv import load_dotenv
from src.database.connection import get_conn

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