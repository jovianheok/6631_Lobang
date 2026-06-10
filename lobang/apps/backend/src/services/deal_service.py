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
                    description,
                    location_name,
                    discount_value,
                    discount_unit,
                    source_url
                FROM public.deals
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
                        "description": row[3],
                        "location_name": row[4],
                        "discount_value": float(row[5]) if row[5] is not None else None,
                        "discount_unit": row[6],
                        "source_url": row[7],
                        "distance_km": None,
                        "score": None,
                    }
                )

            return deals

    finally:
        conn.close()