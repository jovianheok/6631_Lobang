-- Purpose: Drop Lobang app tables for a clean recreate-from-scratch workflow
-- Run this before 001..007 when you want to rebuild the schema from scratch.

DROP POLICY IF EXISTS deal_votes_owner ON public.deal_votes;
DROP POLICY IF EXISTS bookmarks_owner ON public.bookmarks;
DROP POLICY IF EXISTS user_profiles_owner ON public.user_profiles;

DROP TABLE IF EXISTS public.deal_votes;
DROP TABLE IF EXISTS public.bookmarks;
DROP TABLE IF EXISTS public.user_profiles;
DROP TABLE IF EXISTS public.deals;
DROP TABLE IF EXISTS public.raw_deals;
DROP TABLE IF EXISTS public.sources;
