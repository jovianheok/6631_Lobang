"""
Database utility functions for retrieving deals data
from a PostgreSQL database.
"""

# Access environment variables (DATABASE_URL)
import os

# Type hints for better readability and autocomplete support
from typing import Any

# PostgreSQL database adapter for Python
import psycopg2

# Loads variables from .env file into environment
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_conn():
    """
    Create and return a PostgreSQL database connection.

    DATABASE_URL is read from environment variables.
    """
    url = os.getenv("DATABASE_URL", "").strip()
    print("DATABASE_URL repr =", repr(url))
    
    return psycopg2.connect(os.environ["DATABASE_URL"])


def get_deals() -> list[dict[str, Any]]:
    """
    Fetch the latest 50 deals from the database.

    Returns:
        A list of dictionaries whose key is string and value is Any
    """

    # Open database connection
    conn = get_conn()

    try:

        # Create database cursor to execute SQL queries
        with conn.cursor() as cur:

            # Execute SQL query and retrieve latest deals ordered by creation time
                # SELECT: chooses which column to return
                # FROM: from which table
                # ORDER: sorts results; DESC: descending order
                # LIMIT: only returns the first 50 rows after sorting
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

            # Fetch all query results
            rows = cur.fetchall()

            # Store processed deals as a list of dictionaries
            deals: list[dict[str, Any]] = []

            # Convert each database row into a dictionary
            for row in rows:
                deals.append(
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