create table if not exists public.raw_deals (
    id bigserial primary key,

    source_id bigint not null references public.sources(id) on delete restrict, 
    source_url text not null,
    raw_text text not null,
    raw_payload jsonb not null,     -- Store the original structured payload as JSON to preserve original data for reprocessing later
    content_hash text not null,     -- Store a hash of the content to prevent duplication
    
    scraped_at timestamptz not null default now()       -- Store when the data was scraped
);
/* 
'source_id' links each raw deal to a row in the 'sources' table
'reference public.sources(id)': Create a foreign key constraint
In order to insert a raw_deal with a source_id, the source_id has to exist in 'sources' table
'on delete restrict': Cannot delete a source if raw deals still reference it
*/

CREATE UNIQUE INDEX IF NOT EXISTS raw_deals_source_id_content_hash_idx
ON public.raw_deals (source_id, content_hash);
/*
Create a unique index on (source_id, content_hash) so that same source cannot have duplicate content hashes
*/
