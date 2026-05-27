Lobang Technical Design Doc

1. Overview

Lobang is a personalized food deal aggregation app that collects promotions from Telegram channels and restaurant sites, normalizes them into a single canonical schema, ranks them by user relevance, and keeps the feed fresh with scheduled verification and expiry checks.

Core goals

* Aggregate deals from multiple sources
* Normalize and deduplicate them into one database model
* Filter and rank results deterministically
* Support user bookmarks, history, and preferences
* Keep stale deals out of the main feed

⸻

2. Tech stack

* Frontend: Next.js
* Backend: FastAPI
* Database: Supabase Postgres
* Scraping: Python Playwright
* Search/filter/ranking: Python + PostgreSQL queries
* Scheduling: Supabase Cron
* Notifications: Supabase Realtime
* Auth: Supabase Auth
* Uploads: Supabase Storage

⸻

3. High-level architecture

Data flow

1. Supabase Cron triggers scraper jobs.
2. Playwright scrapes source pages or Telegram channels.
3. Raw content is stored in raw_deals.
4. A normalization step converts raw content into canonical deal rows in deals.
5. Deduplication merges or links duplicate records.
6. FastAPI serves filtered and ranked results to Next.js.
7. Supabase Realtime pushes new or updated deals to the frontend.
8. Scheduled verification jobs re-check active deals and update status.

Separation of responsibilities

* Playwright: data collection only
* FastAPI: business logic and API orchestration
* Postgres: truth source for deals and user data
* Next.js: UI and interaction layer

⸻

4. Database schema

Below is a practical schema to start with. It is designed to keep raw data separate from canonical records and user behavior separate from deal content.

4.1 Sources

create table sources (
  id bigserial primary key,
  name text not null,
  source_type text not null check (source_type in ('telegram', 'restaurant_site', 'social', 'other')),
  url text,
  active boolean not null default true,
  trust_score numeric(5,2) not null default 1.0,
  last_scraped_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

4.2 Raw deals

create table raw_deals (
  id bigserial primary key,
  source_id bigint not null references sources(id) on delete cascade,
  source_url text,
  raw_text text not null,
  raw_payload jsonb,
  content_hash text not null,
  scraped_at timestamptz not null default now(),
  created_at timestamptz not null default now(),
  unique (source_id, content_hash)
);

4.3 Canonical deals

create table deals (
  id bigserial primary key,
  source_id bigint not null references sources(id) on delete restrict,
  raw_deal_id bigint references raw_deals(id) on delete set null,
  title text not null,
  description text,
  merchant_name text,
  cuisine_type text,
  deal_type text,
  location_name text,
  address text,
  latitude double precision,
  longitude double precision,
  price_min numeric(10,2),
  price_max numeric(10,2),
  discount_value numeric(10,2),
  discount_unit text,
  eligibility text,
  start_time timestamptz,
  end_time timestamptz,
  status text not null default 'active' check (status in ('active', 'expired', 'inactive', 'unverified')),
  verification_status text not null default 'unverified' check (verification_status in ('unverified', 'verified', 'failed', 'expired')),
  verified_at timestamptz,
  expires_at timestamptz,
  source_url text,
  search_vector tsvector,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

4.4 Deal tags

create table deal_tags (
  deal_id bigint not null references deals(id) on delete cascade,
  tag text not null,
  primary key (deal_id, tag)
);

4.5 Users and preferences

If you are using Supabase Auth, the user identity comes from auth.users. Add a profile table for app-specific fields.

create table user_profiles (
  user_id uuid primary key,
  display_name text,
  home_latitude double precision,
  home_longitude double precision,
  budget_preference numeric(10,2),
  cuisine_preferences text[],
  dietary_preferences text[],
  notification_opt_in boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

4.6 Bookmarks

create table bookmarks (
  user_id uuid not null,
  deal_id bigint not null references deals(id) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (user_id, deal_id)
);

4.7 View history

create table deal_views (
  id bigserial primary key,
  user_id uuid not null,
  deal_id bigint not null references deals(id) on delete cascade,
  viewed_at timestamptz not null default now()
);

4.8 Hidden deals

create table deal_hides (
  user_id uuid not null,
  deal_id bigint not null references deals(id) on delete cascade,
  hidden_at timestamptz not null default now(),
  primary key (user_id, deal_id)
);

4.9 Search queries

create table search_queries (
  id bigserial primary key,
  user_id uuid,
  filters_json jsonb not null,
  created_at timestamptz not null default now()
);

4.10 Verification log

create table deal_verification_events (
  id bigserial primary key,
  deal_id bigint not null references deals(id) on delete cascade,
  verification_status text not null,
  notes text,
  checked_at timestamptz not null default now()
);

⸻

5. Indexes

These indexes make filtering and ranking fast enough for an MVP.

create index idx_deals_status_end_time on deals (status, end_time);
create index idx_deals_location on deals (latitude, longitude);
create index idx_deals_source_id on deals (source_id);
create index idx_bookmarks_user_id on bookmarks (user_id);
create index idx_views_user_id on deal_views (user_id);
create index idx_hides_user_id on deal_hides (user_id);
create index idx_raw_deals_source_hash on raw_deals (source_id, content_hash);

For full-text search:

create index idx_deals_search_vector on deals using gin (search_vector);

You can maintain search_vector with a trigger or in your ingestion pipeline.

⸻

6. Ranking model

Keep ranking deterministic and explainable.

Example weighted score

score =
  0.30 * distance_score +
  0.20 * budget_fit +
  0.20 * cuisine_match +
  0.15 * freshness_score +
  0.10 * timing_fit +
  0.05 * eligibility_score

Suggested scoring components

* distance_score: higher when closer to the user
* budget_fit: higher when the deal matches the user’s target budget
* cuisine_match: higher when the cuisine matches preferences
* freshness_score: higher for recently posted deals
* timing_fit: higher when active now or within the user’s meal window
* eligibility_score: higher when the user meets promo conditions

Return ranking reasons

Return a short explanation with each deal, such as:

* “Nearby and within budget”
* “Matches your preferred cuisine”
* “Recently verified”

That makes the feed more trustworthy and easier to tune.

⸻

7. API design

7.1 Deals feed

GET /deals

Returns a ranked list of deals.

Query params

* lat
* lng
* radius_km
* budget_max
* cuisine
* deal_type
* meal_time
* sort
* page
* limit

Response

{
  "items": [
    {
      "id": 101,
      "title": "2-for-1 lunch set",
      "merchant_name": "Bistro 88",
      "distance_km": 0.8,
      "score": 0.91,
      "status": "active",
      "verification_status": "verified",
      "end_time": "2026-05-21T14:00:00Z",
      "reason": ["Nearby", "Matches your budget", "Recently verified"]
    }
  ],
  "page": 1,
  "limit": 20,
  "total": 128
}

7.2 Deal details

GET /deals/{id}

Returns the full canonical deal record plus provenance.

Response

{
  "id": 101,
  "title": "2-for-1 lunch set",
  "description": "Weekday lunch special...",
  "merchant_name": "Bistro 88",
  "source": {
    "id": 7,
    "name": "Telegram Channel X",
    "url": "https://t.me/..."
  },
  "location": {
    "name": "Bugis",
    "latitude": 1.3001,
    "longitude": 103.8559
  },
  "pricing": {
    "price_min": 12,
    "price_max": 18,
    "discount_value": 10,
    "discount_unit": "%"
  },
  "timing": {
    "start_time": "2026-05-21T00:00:00Z",
    "end_time": "2026-05-21T14:00:00Z"
  },
  "status": "active",
  "verification_status": "verified",
  "source_url": "https://example.com/deal"
}

7.3 Filtered search

POST /deals/filter

Use this for structured filter requests from the frontend.

Request

{
  "lat": 1.3001,
  "lng": 103.8519,
  "radius_km": 3,
  "budget_max": 15,
  "cuisines": ["Japanese", "Asian"],
  "deal_types": ["set_lunch", "discount"],
  "meal_time": "lunch"
}

Response

Same structure as /deals, but may omit ranking reasons if not requested.

7.4 Rank endpoint

POST /deals/rank

Used internally or for debugging ranking changes.

Request

{
  "user_id": "uuid-here",
  "deal_ids": [101, 102, 103],
  "context": {
    "lat": 1.3001,
    "lng": 103.8519,
    "budget_max": 15,
    "meal_time": "lunch"
  }
}

Response

{
  "items": [
    {
      "deal_id": 101,
      "score": 0.91,
      "components": {
        "distance_score": 0.9,
        "budget_fit": 1.0,
        "cuisine_match": 0.8,
        "freshness_score": 0.95,
        "timing_fit": 1.0,
        "eligibility_score": 0.9
      }
    }
  ]
}

7.5 Bookmarks

POST /bookmarks

{ "deal_id": 101 }

DELETE /bookmarks/{deal_id}

Removes the bookmark.

7.6 History

POST /history/view

{ "deal_id": 101 }

7.7 Preferences

POST /users/preferences

{
  "budget_preference": 15,
  "cuisine_preferences": ["Japanese", "Malay"],
  "dietary_preferences": ["halal"]
}

⸻

8. Scraping workflow

Ingestion steps

1. Cron selects active sources.
2. Playwright opens Telegram or restaurant pages.
3. Raw HTML, text, and metadata are extracted.
4. A content hash is created.
5. The raw item is written to raw_deals.
6. A normalizer extracts canonical fields.
7. The canonical deal is upserted into deals.
8. A realtime event updates the feed.

Normalization rules

* Extract merchant name if present
* Extract expiry time if visible
* Parse price and discount fields
* Detect location entities
* Generate a search_vector
* Store all uncertain fields as nullable instead of guessing

⸻

9. Deduplication strategy

Use a layered strategy:

1. Exact hash match on normalized text
2. Same merchant + same time window
3. Near-duplicate title and description similarity
4. Same source URL

Recommended behavior:

* Keep one canonical record
* Link raw records to the canonical deal
* Preserve provenance instead of deleting evidence

⸻

10. Verification and expiry workflow

Scheduled checks

Supabase Cron runs jobs that:

* revisit active deals
* confirm source links still resolve
* confirm timestamps and promo validity
* mark expired deals accordingly

Status transitions

* unverified -> verified
* verified -> expired
* verified -> inactive
* unverified -> failed

Example logic

* If the source page is gone, mark as inactive
* If the deal end time has passed, mark as expired
* If the deal still exists but cannot be confirmed, mark as unverified

⸻

11. Realtime notifications

Use Supabase Realtime for:

* newly inserted deals
* deal status changes
* verification updates
* bookmark and saved-search updates

Frontend behavior:

* subscribe to new active deals matching current filters
* refresh visible lists when a relevant deal changes
* show subtle “new deal found” banners instead of interruptive alerts

⸻

12. Frontend structure

Suggested routes

* / — main feed
* /deal/[id] — deal detail page
* /saved — bookmarked deals
* /history — viewed deals
* /profile — preferences
* /search — advanced filters

UI components

* Deal card
* Filter drawer
* Ranking reason badge
* Save button
* Expiry badge
* Verification badge

⸻

13. Security and permissions

Row-level security

Use RLS for all user-owned tables:

* user_profiles
* bookmarks
* deal_views
* deal_hides
* search_queries

Principle

* Public can read active deals if intended
* Users can only modify their own preferences and history
* Admin or service-role access is required for scraping and verification jobs

⸻

14. MVP implementation order

Phase 1

* Create schema
* Build one scraper for Telegram and one for restaurant sites
* Store raw and canonical deals
* Show a basic deal feed

Phase 2

* Add filters and search
* Add ranking logic
* Add bookmarks and history
* Add login and user preferences

Phase 3

* Add verification jobs
* Add expiry handling
* Add Realtime updates

Phase 4

* Add more sources
* Improve deduplication
* Add screenshots/uploads and community contributions

⸻

15. Recommended first milestone

The best first milestone is:

* one working scraper
* one canonical deal table
* one feed endpoint
* one ranked frontend list
* one bookmark action

That gives you a useful product early and creates the base for everything else.