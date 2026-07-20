-- Purpose: Backfill schema that later CREATE-TABLE migrations (003, 010)
-- introduced but that were never applied to the pre-existing live `deals`
-- table. Without these, GET /api/v1/deals fails with UndefinedColumn.
--
-- Idempotent: ADD COLUMN IF NOT EXISTS / CREATE TABLE IF NOT EXISTS, so it is
-- safe to re-run.
--
-- Note: 003 declares start_date/end_date as NOT NULL, but the live table
-- already holds rows with no value for them, so they are added NULLable here.
-- New inserts from the scraper still always provide a value.

ALTER TABLE public.deals
    ADD COLUMN IF NOT EXISTS more_info_url TEXT,
    ADD COLUMN IF NOT EXISTS image_url     TEXT,
    ADD COLUMN IF NOT EXISTS time_text     TEXT,
    ADD COLUMN IF NOT EXISTS start_date    DATE,
    ADD COLUMN IF NOT EXISTS end_date      DATE;

CREATE INDEX IF NOT EXISTS deals_end_date_idx
ON public.deals (end_date);

-- deal_votes (from 010): one upvote/downvote per user per deal.
CREATE TABLE IF NOT EXISTS public.deal_votes (
    user_id UUID NOT NULL
        REFERENCES auth.users(id) ON DELETE CASCADE,

    deal_id BIGINT NOT NULL
        REFERENCES public.deals(id) ON DELETE CASCADE,

    vote SMALLINT NOT NULL
        CHECK (vote IN (1, -1)),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (user_id, deal_id)
);

CREATE INDEX IF NOT EXISTS deal_votes_deal_id_idx
ON public.deal_votes (deal_id);

ALTER TABLE public.deal_votes ENABLE ROW LEVEL SECURITY;

-- DROP first so the policy create is idempotent (Postgres has no
-- CREATE POLICY IF NOT EXISTS).
DROP POLICY IF EXISTS deal_votes_owner ON public.deal_votes;
CREATE POLICY deal_votes_owner ON public.deal_votes
    FOR ALL
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);
