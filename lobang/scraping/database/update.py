"""
Purpose: Mark status of expired deals to 'expired' to tell frontend not to display
"""

from .connection import get_conn
from .queries import UPDATE_EXPIRED_DEALS

def update_expired_deals() -> int:
    conn = get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(UPDATE_EXPIRED_DEALS)
                expired_rows = cur.fetchall()
                return len(expired_rows)
    finally:
        conn.close()


if __name__ == "__main__":
    count = update_expired_deals()
    print(f"Marked {count} deals as expired.")