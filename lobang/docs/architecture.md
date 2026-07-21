# Lobang Architecture

## Overview

Lobang is a food-deal aggregation app with three main parts:

- A Python scraper/parser pipeline that collects Telegram posts and turns them into structured deals
- A FastAPI backend that reads those deals, applies personalization logic, and exposes REST endpoints
- A Next.js frontend that displays active deals, bookmarks, votes, and personalized recommendations

The system is centered on keeping raw scraped content separate from parsed frontend-facing deal records.

## System Flow

1. The scraper reads posts from the `sgfooddeals` Telegram channel using Playwright.
2. Each scraped post is stored in `raw_deals` with its original text, metadata, image URL, and content hash.
3. The parser reads raw posts, filters for food deals, and extracts structured fields such as title, merchant, more-info URL, image URL, time validity, date validity, and location data.
4. Parsed results are inserted into `deals`, which is the main table consumed by the app.
5. The backend serves active deals from `deals`, joins in vote summaries and user-specific vote state, and applies preference-based ranking for the "For You" feed.
6. The frontend fetches these API responses and renders deal cards with links, images, location badges, validity badges, bookmarks, and voting controls.

## Repository Structure

### `scraping/`

The scraping app is responsible for ingestion and normalization.

- `scrapers/telegram_scraper.py` scrapes Telegram posts and extracts post text, post URL, timestamp, and image URL.
- `parsers/deal_parser.py` orchestrates the parsing pipeline.
- `parsers/_1` to `_9` contain focused extraction steps such as classification, title extraction, merchant extraction, date validity, location, Google Places enrichment, location resolution, more-info URL extraction, and time validity extraction.
- `database/` contains scraping-side database connection, insertion, retrieval, and expiry update helpers.
- `sql/001` to `sql/008` define the schema reset and table creation scripts.

### `apps/backend/`

The backend exposes the application API and user-facing business logic.

- `src/main.py` creates the FastAPI app and registers routes.
- `src/routes/` contains endpoints for deals, bookmarks, preferences, submissions, and votes.
- `src/services/` contains database-backed business logic.
- `src/services/deal_service.py` serves the public deals feed and personalized "For You" feed.
- `src/services/bookmark_service.py` manages saved deals.
- `src/services/vote_service.py` manages deal votes and aggregated vote counts.
- `src/services/submission_service.py` accepts user submissions and runs them through the same parser pipeline as scraped content.
- `src/services/deal_payloads.py` builds a consistent frontend-facing deal response shape across services.
- `src/auth/supabase_auth.py` validates Supabase user tokens for authenticated routes.

### `apps/frontend/`

The frontend is a Next.js app that renders the user interface.

- `app/page.tsx` shows the main deals feed.
- `components/deals-browser.tsx` handles feed fetching, filtering, and feed-state behavior.
- `components/deal-card.tsx` renders each deal card, including image, links, validity badges, bookmark state, and vote controls.
- `lib/api.ts` centralizes calls to the FastAPI backend.
- `lib/supabase.ts` handles frontend Supabase setup for authentication.

## Database Model

The current schema is centered around these tables:

- `sources`: known ingestion sources such as Telegram and user submissions
- `raw_deals`: original scraped or submitted content before parsing
- `deals`: parsed and enriched food deals shown in the app
- `user_profiles`: saved user preferences for personalization
- `bookmarks`: saved deal IDs per user
- `deal_votes`: per-user upvotes and downvotes on deals

### `raw_deals`

This table stores the original content and acts as the ingestion boundary.

Key fields include:

- `source_id`
- `source_url`
- `raw_text`
- `raw_payload`
- `content_hash`
- `scraped_at`

Duplicate raw posts are prevented with a unique constraint on `(source_id, content_hash)`.

### `deals`

This table stores parsed, enriched, frontend-facing deal data.

Key fields include:

- `raw_deal_id`
- `source_id`
- `source_url`
- `content_hash`
- `title`
- `merchant_name`
- `more_info_url`
- `image_url`
- `time_text`
- `start_date`
- `end_date`
- `cuisine`
- `price_level`
- `address`
- `outlet_count`
- `covered_regions`
- `location_text`
- `display_location`
- `location_mode`
- `status`

Duplicate parsed deals are likewise prevented with `(source_id, content_hash)`.

## Parsing Pipeline

The parser is intentionally split into small steps so each concern is easier to test and evolve.

- Classification filters out posts that are not food deals.
- Title and merchant extraction turn unstructured post text into a cleaner card heading.
- Date validity extraction produces `start_date` and `end_date`.
- Time validity extraction produces `time_text` only when an explicit time window is present.
- More-info URL extraction captures merchant or campaign links from the raw text.
- Image extraction happens at scrape time and is passed through the parser into `deals`.
- Location extraction and resolution determine what location information should be shown to the frontend.
- Google Places enrichment adds cuisine, price level, address, and outlet coverage where possible.

## Personalization And Voting

The backend currently exposes two main feed modes:

- `GET /api/v1/deals`: latest active deals
- `GET /api/v1/deals/for-you`: preference-ranked deals for an authenticated user

The "For You" feed uses:

- max price level as a hard filter when both user and deal price are known
- cuisine preference matches as a positive ranking signal
- preferred region matches as a positive ranking signal
- community vote score as a light ranking signal once a deal has enough votes

Votes are stored per `(user_id, deal_id)` in `deal_votes`, and the backend returns both aggregate vote counts and the current user's own vote state.

## User Features

The current frontend/backend flow supports:

- browsing active deals
- viewing images and external links
- bookmarks
- user preferences
- personalized recommendations
- community upvotes and downvotes
- authenticated user submissions

## Current Scope

This document reflects the architecture currently implemented in the repository as of July 21, 2026. Earlier ideas such as realtime pushes, verification logs, hidden deals, and broader multi-source ingestion may still be future enhancements, but they are not part of the current code path and are therefore not treated as core architecture here.
