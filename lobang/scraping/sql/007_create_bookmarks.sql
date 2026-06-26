-- Deals a user has saved. Composite PK prevents duplicate bookmarks.

CREATE TABLE IF NOT EXISTS public.bookmarks (
    user_id UUID NOT NULL
        REFERENCES auth.users(id) ON DELETE CASCADE,
    deal_id BIGINT NOT NULL
        REFERENCES public.deals(id) ON DELETE CASCADE,
        -- Drop the bookmark automatically if the deal is removed
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (user_id, deal_id)
);

CREATE INDEX IF NOT EXISTS idx_bookmarks_user_id
    ON public.bookmarks (user_id);

ALTER TABLE public.bookmarks ENABLE ROW LEVEL SECURITY;

CREATE POLICY bookmarks_owner ON public.bookmarks
    FOR ALL
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);
