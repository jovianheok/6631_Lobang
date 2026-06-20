"""
Purpose: Hold SQL strings for storage.py to execute at runtime
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
ON CONFLICT (source_id, content_hash) DO NOTHING
RETURNING id;
"""

RETRIEVE_RAW_POST = """
SELECT 
id,
raw_text,
scraped_at

FROM raw_posts
ORDER BY scraped_at DESC
"""

INSERT_PARSED_DEAL = """
INSERT INTO deals (
    raw_deal_id,
    source_id,
    content_hash,
    title,
    description,
    merchant_name,
    source_url
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (source_id, content_hash) DO NOTHING
RETURNING id;
"""