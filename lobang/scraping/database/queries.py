"""
Purpose: Hold SQL strings for insertion.py, retrieval.py and cleanup.py
"""

INSERT_RAW_POST = """
INSERT INTO raw_deals (
    source_id,
    source_url,
    raw_text,
    raw_payload,
    content_hash,
    scraped_at
)
VALUES (%s, %s, %s, %s, %s, now())
ON CONFLICT (source_id, content_hash) DO UPDATE SET
    source_url = EXCLUDED.source_url,
    raw_text = EXCLUDED.raw_text,
    raw_payload = EXCLUDED.raw_payload,
    scraped_at = NOW()
RETURNING id;
"""

RETRIEVE_RAW_POST = """
SELECT
    id,
    source_url,
    raw_text,
    raw_payload,
    content_hash,
    scraped_at
FROM raw_deals
ORDER BY scraped_at DESC;
"""

INSERT_PARSED_DEAL = """
INSERT INTO deals (
    raw_deal_id,
    source_id,
    source_url,
    content_hash,
    more_info_url,
    image_url,
    time_text,
    title,
    merchant_name,
    start_date,
    end_date,
    cuisine,
    price_level,
    address,
    outlet_count,
    covered_regions,
    location_text,
    display_location,
    location_mode,
    status
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (source_id, content_hash) DO UPDATE SET
    more_info_url = COALESCE(deals.more_info_url, EXCLUDED.more_info_url),
    image_url = COALESCE(EXCLUDED.image_url, deals.image_url),
    time_text = COALESCE(deals.time_text, EXCLUDED.time_text),
    source_url = COALESCE(deals.source_url, EXCLUDED.source_url),
    title = COALESCE(deals.title, EXCLUDED.title),
    merchant_name = COALESCE(deals.merchant_name, EXCLUDED.merchant_name),
    start_date = COALESCE(deals.start_date, EXCLUDED.start_date),
    end_date = COALESCE(deals.end_date, EXCLUDED.end_date),
    cuisine = COALESCE(deals.cuisine, EXCLUDED.cuisine),
    price_level = COALESCE(deals.price_level, EXCLUDED.price_level),
    address = COALESCE(deals.address, EXCLUDED.address),
    outlet_count = CASE
        WHEN deals.outlet_count = 0 THEN EXCLUDED.outlet_count
        ELSE deals.outlet_count
    END,
    covered_regions = CASE
        WHEN COALESCE(array_length(deals.covered_regions, 1), 0) = 0 THEN EXCLUDED.covered_regions
        ELSE deals.covered_regions
    END,
    location_text = COALESCE(deals.location_text, EXCLUDED.location_text),
    display_location = COALESCE(deals.display_location, EXCLUDED.display_location),
    location_mode = COALESCE(deals.location_mode, EXCLUDED.location_mode)
RETURNING id;
"""

UPDATE_EXPIRED_DEALS = """
UPDATE deals
SET status = 'expired',
    expired_at = NOW()
WHERE status = 'active'
  AND end_date < CURRENT_DATE
RETURNING id;
"""
