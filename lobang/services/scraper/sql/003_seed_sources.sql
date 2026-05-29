insert into public.sources (platform, channel_name, url)    -- Insert a new row into the sources table
values ('telegram',                                         --   specifying platform,
        'sgfooddeals',                                      --   channel_name,
        'https://t.me/s/sgfooddeals'                        --   and url
)
on conflict (platform, channel_name) do nothing;            -- Skip the insert if inserting the row violates the unique constraint