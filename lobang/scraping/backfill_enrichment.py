"""
Purpose: Re-run Google Places enrichment for deals that are missing it.

Deals inserted by a pipeline run where Places enrichment did not happen (no
GOOGLE_PLACES_API_KEY loaded, quota exhausted, network failure) keep NULL
cuisine / price_level / address and an empty covered_regions. Those columns are
what the Home filters and the For You score read, so such deals match nothing
and score 0.

This re-parses the stored raw_deals rows behind those deals — no re-scrape — and
saves them back through the normal upsert, which only fills in columns that are
still empty (see INSERT_PARSED_DEAL's COALESCE clauses).

Usage (from lobang/scraping, needs DATABASE_URL + GOOGLE_PLACES_API_KEY in .env):
    python3 backfill_enrichment.py --dry-run   # show what would be filled in
    python3 backfill_enrichment.py             # write it
"""

import sys
from collections import defaultdict

from database.connection import get_conn
from database.insertion import save_parsed_deals
from database.retrieval import get_raw_posts
from parsers.deal_parser import parse_raw_post

SELECT_UNENRICHED_DEALS = """
SELECT id, raw_deal_id, source_id, merchant_name
FROM deals
WHERE status = 'active'
  AND raw_deal_id IS NOT NULL
  AND (
      cuisine IS NULL
      OR price_level IS NULL
      OR address IS NULL
      OR COALESCE(array_length(covered_regions, 1), 0) = 0
  )
ORDER BY id;
"""


def get_unenriched_deals() -> list[dict]:
    """
    Return the active deals still missing at least one enrichment column.
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(SELECT_UNENRICHED_DEALS)
            return [
                {
                    "deal_id": row[0],
                    "raw_deal_id": row[1],
                    "source_id": row[2],
                    "merchant_name": row[3],
                }
                for row in cur.fetchall()
            ]
    finally:
        conn.close()


def main(dry_run: bool = False) -> None:
    targets = get_unenriched_deals()
    if not targets:
        print("Nothing to backfill: every active deal already has enrichment.")
        return

    by_raw_deal_id = {target["raw_deal_id"]: target for target in targets}
    print(f"{len(targets)} active deals missing enrichment.")

    raw_posts = {row["id"]: row for row in get_raw_posts()}

    # Group by source_id: the deals upsert keys on (source_id, content_hash), so
    # saving with the wrong source_id would insert a duplicate instead of filling
    # the existing row in.
    parsed_by_source: dict[int, list[dict]] = defaultdict(list)
    skipped = 0

    for raw_deal_id, target in by_raw_deal_id.items():
        raw_post = raw_posts.get(raw_deal_id)
        if raw_post is None:
            print(f"  deal {target['deal_id']}: raw post {raw_deal_id} is gone, skipped")
            skipped += 1
            continue

        parsed = parse_raw_post(raw_post)
        if parsed is None:
            print(f"  deal {target['deal_id']}: raw post no longer parses as a deal, skipped")
            skipped += 1
            continue

        merchant = parsed.get("merchant_name") or "(no merchant name)"
        print(
            f"  deal {target['deal_id']}: {merchant} -> "
            f"cuisine={parsed.get('cuisine')} "
            f"price_level={parsed.get('price_level')} "
            f"regions={parsed.get('covered_regions')}"
        )
        parsed_by_source[target["source_id"]].append(parsed)

    if dry_run:
        total = sum(len(deals) for deals in parsed_by_source.values())
        print(f"\nDry run: would update {total} deals, skipped {skipped}. Nothing written.")
        return

    updated = 0
    for source_id, deals in parsed_by_source.items():
        updated += len(save_parsed_deals(deals, source_id=source_id))

    print(f"\nDone. Updated {updated}, skipped {skipped}.")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
