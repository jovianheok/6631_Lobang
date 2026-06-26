"""
Purpose: One-off backfill of enrichment columns (cuisine, price_level, address,
outlet coverage, location) on deals that were inserted before the Google Places
enrichment pipeline existed.

It re-parses each deal's original raw post via parse_raw_post (which performs the
Google Places lookups) and updates ONLY the enrichment columns, leaving
title / merchant_name / expiry / status untouched.

Run from the scraping/ directory:

    python backfill_enrichment.py

Reads DATABASE_URL and GOOGLE_PLACES_API_KEY from scraping/.env. The Google
Places calls may incur cost / consume quota, so this is intentionally a manual,
one-off script rather than part of the regular pipeline.
"""

from psycopg2.extras import RealDictCursor

from database.connection import get_conn
from parsers.deal_parser import parse_raw_post

# Deals still missing enrichment, joined to their original raw post. Aliased so
# the row dict matches what parse_raw_post expects:
# id, source_url, raw_text, content_hash, scraped_at.
SELECT_DEALS_TO_BACKFILL = """
SELECT
    d.id            AS deal_id,
    r.id            AS id,
    r.source_url    AS source_url,
    r.raw_text      AS raw_text,
    r.content_hash  AS content_hash,
    r.scraped_at    AS scraped_at
FROM public.deals d
JOIN public.raw_deals r ON r.id = d.raw_deal_id
WHERE d.cuisine IS NULL
  AND d.price_level IS NULL
  AND d.location_mode IS NULL
ORDER BY d.id;
"""

UPDATE_DEAL_ENRICHMENT = """
UPDATE public.deals
SET cuisine          = %s,
    price_level      = %s,
    address          = %s,
    outlet_count     = %s,
    covered_regions  = %s,
    location_text    = %s,
    display_location = %s,
    location_mode    = %s
WHERE id = %s;
"""


def backfill() -> None:
    conn = get_conn()
    updated = 0
    skipped = 0
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(SELECT_DEALS_TO_BACKFILL)
            rows = cur.fetchall()

        print(f"Found {len(rows)} deal(s) needing enrichment")

        for row in rows:
            deal_id = row["deal_id"]
            parsed = parse_raw_post(row)  # runs Google Places enrichment

            if not parsed:
                skipped += 1
                print(f"  deal {deal_id}: parser returned nothing, skipped")
                continue

            with conn.cursor() as cur:
                cur.execute(
                    UPDATE_DEAL_ENRICHMENT,
                    (
                        parsed.get("cuisine"),
                        parsed.get("price_level"),
                        parsed.get("address"),
                        parsed.get("outlet_count"),
                        parsed.get("covered_regions") or [],
                        parsed.get("location_text"),
                        parsed.get("display_location"),
                        parsed.get("location_mode"),
                        deal_id,
                    ),
                )
            conn.commit()
            updated += 1
            print(
                f"  deal {deal_id}: cuisine={parsed.get('cuisine')} "
                f"price_level={parsed.get('price_level')} "
                f"regions={parsed.get('covered_regions')}"
            )

        print(f"\nDone. Updated {updated}, skipped {skipped}.")
    finally:
        conn.close()


if __name__ == "__main__":
    backfill()
