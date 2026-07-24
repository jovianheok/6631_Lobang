-- App-specific user data, keyed to Supabase Auth identity.
-- Holds the three personalization preferences: price level, cuisine, location.
-- Location is stored two ways: predefined regions AND a home point + radius.

CREATE TABLE IF NOT EXISTS public.user_profiles (
    user_id UUID PRIMARY KEY
        REFERENCES auth.users(id) ON DELETE CASCADE,
    -- One profile per authenticated user; remove profile if the account is deleted

    display_name TEXT,

    -- Price preference: 0..4 (matches deals.price_level / Google Places). NULL = no preference
    max_price_level INT
        CHECK (max_price_level BETWEEN 0 AND 4),

    -- Cuisine preference: canonical cuisine labels (see enricher CUISINE_TYPE_MAP)
    cuisine_preferences TEXT[] NOT NULL DEFAULT '{}',

    -- Location, region model: predefined SG regions
    preferred_regions TEXT[] NOT NULL DEFAULT '{}',

    -- Location, distance model: a home point + how far the user will travel
    home_latitude DOUBLE PRECISION,
    home_longitude DOUBLE PRECISION,
    max_distance_km NUMERIC(6, 2),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Defense in depth: the backend already scopes every query by user_id,
-- but RLS guarantees no row leaks if the anon key ever touches this table.
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_profiles_owner ON public.user_profiles
    FOR ALL
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);
