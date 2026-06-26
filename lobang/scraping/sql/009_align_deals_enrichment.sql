-- Align an existing deals table with the enriched schema defined in
-- 003_create_deals_table.sql (Google Places enrichment + location resolution).
-- Needed for databases whose deals table predates these columns; 003 uses
-- CREATE TABLE IF NOT EXISTS and so will not alter an existing table.
-- Idempotent: ADD COLUMN IF NOT EXISTS + guarded constraint adds.

ALTER TABLE public.deals
    ADD COLUMN IF NOT EXISTS cuisine TEXT,
    ADD COLUMN IF NOT EXISTS price_level INT,
    ADD COLUMN IF NOT EXISTS address TEXT,
    ADD COLUMN IF NOT EXISTS outlet_count INT NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS covered_regions TEXT[] NOT NULL DEFAULT '{}',
    ADD COLUMN IF NOT EXISTS location_text TEXT,
    ADD COLUMN IF NOT EXISTS display_location TEXT,
    ADD COLUMN IF NOT EXISTS location_mode TEXT;

-- ADD CONSTRAINT has no IF NOT EXISTS, so add the CHECKs only when missing.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'deals_price_level_check'
    ) THEN
        ALTER TABLE public.deals
            ADD CONSTRAINT deals_price_level_check
            CHECK (price_level IS NULL OR price_level BETWEEN 0 AND 4);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'deals_location_mode_check'
    ) THEN
        ALTER TABLE public.deals
            ADD CONSTRAINT deals_location_mode_check
            CHECK (location_mode IS NULL OR location_mode IN
                ('explicit', 'coverage', 'islandwide', 'hidden'));
    END IF;
END $$;
