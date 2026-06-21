create table if not exists public.sources (

    id bigserial primary key,       -- Create a column named 'id', 'primary key': makes id the unique identifier for each row
    platform text not null,
    channel_name text not null,
    url text,
    created_at timestamptz not null default now(),

    unique(platform, channel_name)      -- Create a unique index behind the scenes to enforce the constraint
);