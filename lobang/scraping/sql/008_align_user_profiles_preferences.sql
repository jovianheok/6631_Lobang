-- Align an existing user_profiles table with the preference columns the backend
-- expects (see 006_create_user_profiles.sql). Safe to run on databases whose
-- user_profiles predates 006 and lacks these columns; ADD COLUMN IF NOT EXISTS
-- makes it a no-op where they already exist.
ALTER TABLE public.user_profiles
      ADD COLUMN IF NOT EXISTS max_price_level int
          CHECK (max_price_level BETWEEN 0 AND 4),   -- 0..4, NULL = no preference
      ADD COLUMN IF NOT EXISTS preferred_regions text[] NOT NULL DEFAULT '{}',
      ADD COLUMN IF NOT EXISTS max_distance_km numeric(6,2);
