"""
Purpose: Retrieve raw posts from database
"""

from database.connection import get_conn
from .queries import RETRIEVE_RAW_POST
from psycopg2.extras import RealDictCursor


def get_raw_posts():
    """
    Purpose: Retrieve raw posts from database
    """
    conn = get_conn()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(RETRIEVE_RAW_POST)
            return cursor.fetchall()

    finally:
        conn.close()