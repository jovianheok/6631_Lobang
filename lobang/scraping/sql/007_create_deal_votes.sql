-- Purpose: Create 'deal_votes' table to store one upvote/downvote per user per deal

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

CREATE POLICY deal_votes_owner ON public.deal_votes
    FOR ALL
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);
