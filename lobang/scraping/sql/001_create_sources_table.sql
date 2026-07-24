-- Purpose: Create 'sources' table to store upstream scraping sources

CREATE TABLE IF NOT EXISTS public.sources (
    id BIGSERIAL PRIMARY KEY,

    platform TEXT NOT NULL,
    channel_name TEXT NOT NULL,
    url TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT sources_platform_channel_name_uniq
        UNIQUE (platform, channel_name)
);
