# Lobang

Personalized food deal aggregation platform.

## Stack

- Next.js
- FastAPI
- Supabase
- Playwright

## Development

TBD

## Testing

- to launch backend: inside apps/backend, run "uvicorn src.main:app --reload"
- to launch frontend: inside apps/frontend, run "npm run dev"

## Frontend-to-Backend
1. Frontend JS getDeals()
2. getDeals() calls fetch()
3. Browser creates an HTTP request
4. Request arrives at Uvicorn
5. FastAPI matches the route
6. Backend Python list_deals() runs
7. FastAPI converts Python into HTTP response
8. Browser receives response

## Flow
1. Scrape raw posts on telegram channel ✅
2. Save raw_deals to PostgreSQL database ✅
3. Parse raw_deals ✅
4. Save parsed_deals to PostgreSQL database
5. Add enrichment
6. Build API for frontend to query deals from database