create table if not exists public.sources (             -- Create a table named 'sources'
--                                                         'if not exists' prevents an error if the table already exists

    id bigserial primary key,                           -- Create a column named 'id'
    --                                                     'bigserial': auto-incrementing 64-bit integer
    --                                                     'primary key': makes id the unique identifier for each row

    platform text not null,                             -- Create a 'platform' column

    channel_name text not null,                         -- Create a 'channel_name' column

    url text,                                           -- Create a 'url' column

    created_at timestamptz not null default now(),      -- Create a timestamp column
    --                                                     'timestamptz': timestamp with timezone awareness
    --                                                     'default now()': stores the current timestamp when a row is inserted

    unique(platform, channel_name)                      -- Create a unique index behind the scenes to enforce the constraint
);