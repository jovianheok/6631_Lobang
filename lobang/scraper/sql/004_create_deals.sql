create table if not exists public.deals (
    id bigserial primary key,
    raw_deal_id bigint references public.raw_deals(id) on delete set null,
    /*
    Link a structured deal back to the original raw scraped data
    'on delete set null': Set raw_deal_id to NULL instead of deleting the deal if the referenced raw_deal is deleted
    */

    source_id bigint not null references public.sources(id) on delete restrict,
    /*
    Link the deal to its source
    'on delete restrict': Cannot delete a source if deals still reference it
    */

    content_hash text not null,

    title text not null,
    description text,

    merchant_name text,
    location_name text,

    discount_value numeric(10,2),       -- Up to 10 digits total and 2 decimal places
    discount_unit text,

    source_url text,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create unique index if not exists deals_source_id_content_hash_idx
on public.deals (source_id, content_hash);