"""
Purpose: Accept user-submitted deals and run them through the same parsing
pipeline as scraped Telegram posts (classification, extraction, enrichment),
so user deals get identical checks and data quality.
"""

import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from psycopg2.extras import Json

from src.database.connection import get_conn

# The parsing pipeline lives in the sibling scraping app (lobang/scraping) and
# imports its modules as top-level "parsers.*", so its directory must be on
# sys.path before importing. Requires GOOGLE_PLACES_API_KEY in this app's .env
# for enrichment (degrades gracefully to unenriched deals without it).
SCRAPING_DIR = Path(__file__).resolve().parents[4] / "scraping"
if str(SCRAPING_DIR) not in sys.path:
    sys.path.insert(0, str(SCRAPING_DIR))

from parsers.deal_parser import parse_raw_post  # noqa: E402

# All site submissions share one row in public.sources, created on first use
# (the Telegram scraper is source_id 1).
USER_SOURCE_PLATFORM = "web"
USER_SOURCE_CHANNEL = "user_submissions"


class NotAFoodDealError(Exception):
    """The submission failed the same is_food_deal check scraped posts go through."""


class DuplicateSubmissionError(Exception):
    """An identical submission already exists."""


def _get_or_create_source_id(cur) -> int:
    """Return the user-submissions source id, inserting the row on first use."""
    cur.execute(
        "SELECT id FROM public.sources WHERE platform = %s AND channel_name = %s;",
        (USER_SOURCE_PLATFORM, USER_SOURCE_CHANNEL),
    )
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO public.sources (platform, channel_name) VALUES (%s, %s) RETURNING id;",
        (USER_SOURCE_PLATFORM, USER_SOURCE_CHANNEL),
    )
    return cur.fetchone()[0]


def submit_deal(
    user_id: str,
    merchant_name: str,
    description: str,
    more_info_url: Optional[str] = None,
) -> dict[str, Any]:
    """
    Store a user submission as a raw deal, parse it exactly like a scraped post,
    and publish the resulting deal. Returns the new deal shaped like DealOut.

    Raises NotAFoodDealError if classification rejects the text and
    DuplicateSubmissionError if an identical submission already exists. Both
    roll back the whole transaction, so a rejected submission leaves no rows
    behind and can be edited and resubmitted.
    """
    merchant_name = merchant_name.strip()
    description = description.strip()
    more_info_url = (more_info_url or "").strip() or None

    # "Merchant: description" is the strongest merchant signal the parser knows
    # (the title-prefix rule), so structured form input feeds the unstructured
    # pipeline reliably. The link goes on its own line for URL extraction.
    raw_text = f"{merchant_name}: {description}"
    if more_info_url:
        raw_text += f"\n{more_info_url}"

    # Global hash over the assembled text so identical submissions dedupe via
    # the (source_id, content_hash) constraint, mirroring the scraper's hashing.
    content_hash = hashlib.sha256(
        f"user-submission|{raw_text.strip()}".encode("utf-8")
    ).hexdigest()
    source_url = more_info_url or "user-submission"
    now = datetime.now(timezone.utc)

    conn = get_conn()
    try:
        with conn:  # one transaction: reject/duplicate rolls everything back
            with conn.cursor() as cur:
                source_id = _get_or_create_source_id(cur)

                cur.execute(
                    """
                    INSERT INTO public.raw_deals (
                        source_id, source_url, raw_text, raw_payload,
                        content_hash, scraped_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (source_id, content_hash) DO NOTHING
                    RETURNING id;
                    """,
                    (
                        source_id,
                        source_url,
                        raw_text,
                        # submitted_by lives in the payload, so no schema change.
                        Json(
                            {
                                "merchant_name": merchant_name,
                                "description": description,
                                "more_info_url": more_info_url,
                                "submitted_by": user_id,
                            }
                        ),
                        content_hash,
                        now,
                    ),
                )
                row = cur.fetchone()
                if row is None:
                    raise DuplicateSubmissionError()
                raw_deal_id = row[0]

                # Same checks as Telegram posts: classification, title/merchant,
                # expiry, location, Places enrichment, region coverage.
                parsed = parse_raw_post(
                    {
                        "id": raw_deal_id,
                        "source_url": source_url,
                        "raw_text": raw_text,
                        "content_hash": content_hash,
                        "scraped_at": now,
                    }
                )
                if parsed is None:
                    raise NotAFoodDealError()

                # Trust the form over extraction for fields the user gave us.
                parsed["merchant_name"] = merchant_name
                if more_info_url:
                    parsed["more_info_url"] = parsed.get("more_info_url") or more_info_url

                cur.execute(
                    """
                    INSERT INTO public.deals (
                        raw_deal_id, source_id, source_url, content_hash,
                        more_info_url, title, merchant_name, expiry_date,
                        display_until, cuisine, price_level, address,
                        outlet_count, covered_regions, location_text,
                        display_location, location_mode, status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (source_id, content_hash) DO NOTHING
                    RETURNING id;
                    """,
                    (
                        raw_deal_id,
                        source_id,
                        parsed.get("source_url"),
                        parsed.get("content_hash"),
                        parsed.get("more_info_url"),
                        parsed.get("title"),
                        parsed.get("merchant_name"),
                        parsed.get("expiry_date"),
                        parsed.get("display_until"),
                        parsed.get("cuisine"),
                        parsed.get("price_level"),
                        parsed.get("address"),
                        parsed.get("outlet_count") or 0,
                        parsed.get("covered_regions") or [],
                        parsed.get("location_text"),
                        parsed.get("display_location"),
                        parsed.get("location_mode"),
                        "active",
                    ),
                )
                row = cur.fetchone()
                if row is None:
                    raise DuplicateSubmissionError()

                return {
                    "id": row[0],
                    "title": parsed.get("title"),
                    "merchant_name": parsed.get("merchant_name"),
                    "source_url": parsed.get("source_url"),
                    "more_info_url": parsed.get("more_info_url"),
                    "cuisine": parsed.get("cuisine"),
                    "price_level": parsed.get("price_level"),
                    "address": parsed.get("address"),
                    "covered_regions": parsed.get("covered_regions") or [],
                    "display_location": parsed.get("display_location"),
                }
    finally:
        conn.close()
