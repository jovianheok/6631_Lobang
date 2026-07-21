-- Purpose: Seed default scraping sources

INSERT INTO public.sources (platform, channel_name, url)
VALUES (
    'telegram',
    'sgfooddeals',
    'https://t.me/s/sgfooddeals'
)
ON CONFLICT (platform, channel_name) DO NOTHING;
