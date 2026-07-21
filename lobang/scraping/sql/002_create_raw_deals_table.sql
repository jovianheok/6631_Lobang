-- Purpose: Create 'raw_deals' table to store raw deals scraped from Telegram

CREATE TABLE IF NOT EXISTS public.raw_deals (
    id BIGSERIAL PRIMARY KEY,

    source_id BIGINT NOT NULL
        REFERENCES public.sources(id) ON DELETE RESTRICT,
    -- Source channel or submission origin

    source_url TEXT NOT NULL,

    raw_text TEXT NOT NULL,

    raw_payload JSONB NOT NULL,
    -- Original Telegram payload

    content_hash TEXT NOT NULL,
    -- Used for deduplication

    scraped_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- When the post was scraped

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    -- When the raw row was inserted
);

CREATE UNIQUE INDEX IF NOT EXISTS raw_deals_source_id_content_hash_idx
ON public.raw_deals (source_id, content_hash);
-- Prevent duplicate posts from the same source

CREATE INDEX IF NOT EXISTS raw_deals_scraped_at_idx
ON public.raw_deals (scraped_at DESC);
-- Speed up retrieval of recent posts
