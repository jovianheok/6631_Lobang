ALTER TABLE public.deals
      ADD COLUMN IF NOT EXISTS cuisine text,
      ADD COLUMN IF NOT EXISTS price_level int,
      ADD COLUMN IF NOT EXISTS address text;
