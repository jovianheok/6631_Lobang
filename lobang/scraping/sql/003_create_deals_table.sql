-- Purpose: Create 'deals' table to store parsed and enriched deals

CREATE TABLE IF NOT EXISTS public.deals (
    id BIGSERIAL PRIMARY KEY,

    raw_deal_id BIGINT
        REFERENCES public.raw_deals(id) ON DELETE SET NULL,
    -- Link back to the original raw post

    source_id BIGINT NOT NULL
        REFERENCES public.sources(id) ON DELETE RESTRICT,
    -- Source channel

    source_url TEXT,

    content_hash TEXT NOT NULL,

    more_info_url TEXT,
    -- Parsed external link from "More info" / "Find out more" in the raw post
    image_url TEXT,
    -- Telegram post image URL when the post includes a photo

    title TEXT NOT NULL,
    merchant_name TEXT,

    expiry_date DATE,
    -- Actual expiry extracted from the post

    display_until DATE NOT NULL,
    -- Hide the deal after this date

    cuisine TEXT,
    price_level INT,
    address TEXT,

    outlet_count INT NOT NULL DEFAULT 0,
    -- Number of unique Places results returned

    covered_regions TEXT[] NOT NULL DEFAULT '{}',
    -- Regions covered by the merchant

    location_text TEXT,
    -- Explicit location extracted from the post

    display_location TEXT,
    -- Frontend display location

    location_mode TEXT,

    status TEXT NOT NULL DEFAULT 'active',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- When the deal was created

    expired_at TIMESTAMPTZ,
    -- When the deal was marked expired

    CONSTRAINT deals_source_hash_uniq
        UNIQUE (source_id, content_hash),

    CONSTRAINT deals_price_level_check
        CHECK (price_level IS NULL OR price_level BETWEEN 0 AND 4),

    CONSTRAINT deals_location_mode_check
        CHECK (location_mode IS NULL OR location_mode IN ('explicit', 'coverage', 'islandwide','hidden')),

    CONSTRAINT deals_status_check
        CHECK (status IN ('active', 'expired'))
);

CREATE INDEX IF NOT EXISTS deals_status_idx
ON public.deals (status);
-- Speed up filtering active deals

CREATE INDEX IF NOT EXISTS deals_display_until_idx
ON public.deals (display_until);
-- Speed up expiry updates
