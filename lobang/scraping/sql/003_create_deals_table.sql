CREATE TABLE IF NOT EXISTS public.deals (
    id BIGSERIAL PRIMARY KEY,

    raw_deal_id BIGINT REFERENCES public.raw_deals(id) ON DELETE SET NULL,
    -- Link a structured deal back to the original raw scraped data
    -- 'on delete set null': Set raw_deal_id to NULL instead of deleting the deal if the referenced raw_deal is deleted
    source_id BIGINT NOT NULL REFERENCES public.sources(id) ON DELETE RESTRICT,
    -- Link the deal to its source
    -- 'on delete restrict': Cannot delete a source if deals still reference it
    source_url TEXT,
    content_hash TEXT NOT NULL,
    
    title TEXT NOT NULL,
    merchant_name TEXT,

    expiry_date DATE,       -- actual expiry extracted from the post
    display_until DATE NOT NULL,        -- date after which we hide the post

    status TEXT NOT NULL DEFAULT 'active',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expired_at TIMESTAMPTZ

    cuisine text,
    price_level int,
    address text;
    

);

CREATE UNIQUE INDEX IF NOT EXISTS deals_source_id_content_hash_idx
ON public.deals (source_id, content_hash);