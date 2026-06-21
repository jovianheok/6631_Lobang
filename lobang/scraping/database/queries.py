"""
Purpose: Hold SQL strings for insertion.py, retrieval.py and cleanup.py to execute at runtime
"""

INSERT_RAW_POST = """
INSERT INTO raw_deals (
    source_id, source_url, raw_text, raw_payload, content_hash, scraped_at
)
VALUES (%s, %s, %s, %s, %s, now())
ON CONFLICT (source_id, content_hash) DO NOTHING
RETURNING id;
"""

RETRIEVE_RAW_POST = """
SELECT 
    id, source_url, raw_text, content_hash, scraped_at
FROM raw_deals
ORDER BY scraped_at DESC
"""

INSERT_PARSED_DEAL = """
INSERT INTO deals (
    raw_deal_id, source_id, source_url, content_hash,
    title, merchant_name, expiry_date, display_until, status
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (source_id, content_hash) DO NOTHING
RETURNING id;
"""

UPDATE_EXPIRED_DEALS = """
UPDATE deals
SET status = 'expired',
    expired_at = NOW()
WHERE status = 'active'
  AND display_until < CURRENT_DATE
RETURNING id;
"""