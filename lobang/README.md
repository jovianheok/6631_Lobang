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
- Launch backend:
    cd apps/backend
    source .venv/bin/activate
    uvicorn src.main:app --reload

- Launch frontend:
    cd apps/frontend
    npm run dev

- Launch scraper and parser:
    cd services/scraper
    source .venv/bin/activate
    python main.py

## Frontend-to-Backend
1. When you start the backend using a command such as uvicorn src.main:app --reload, FastAPI loads main.py, creates the app object, registers all routers, and begins listening for incoming requests on http://127.0.0.1:8000. At this stage, no data has been requested yet—the backend is simply waiting for requests. 

2. Next, when you start the frontend using a command such as npm run dev, Next.js launches its development server and serves the application. 

3. When a user opens the homepage in their browser, Next.js executes the HomePage() function in page.tsx. Inside HomePage(), the code calls getDeals() from lib/api.ts, which sends an HTTP GET request to http://127.0.0.1:8000/api/v1/deals. 

4. The backend receives this request through the FastAPI application defined in main.py. Because main.py registered api_router using app.include_router(api_router, prefix="/api/v1"), FastAPI knows that requests beginning with /api/v1 should be handled by api_router. 

5. In router.py, api_router.include_router(deals_router) registers all routes from deals.py, allowing FastAPI to find the matching endpoint @router.get("/deals"). 

6. FastAPI then executes the list_deals() function, which calls get_deals() in deal_service.py. This service function opens a PostgreSQL database connection, executes a SQL query to retrieve the latest 50 deals from the public.deals table, and converts the returned rows into Python dictionaries. 

7. The data is returned to FastAPI, validated against the DealOut schema, converted into JSON, and sent back as the HTTP response. The frontend receives this JSON response in getDeals(), converts it into JavaScript objects using response.json(), and returns it to HomePage(). 

8. Finally, HomePage() loops through the deals using deals.map(...), passes each deal's information into a DealCard component, and Next.js renders the completed list of deal cards in the browser for the user to view.

## Flow
1. Scrape raw posts on telegram channel ✅
2. Save raw_deals to PostgreSQL database ✅
3. Parse raw_deals ✅
4. Save parsed_deals to PostgreSQL database ✅
5. Add enrichment
6. Build API for frontend to query deals from database

# Deployment plan
Frontend on Vercel → calls backend URL → backend on Render → backend reads DATABASE_URL → backend talks to PostgreSQL → backend returns JSON → frontend renders the cards.

# Git commit messages
feat: A new feature for the application or library.
fix: A patch or bug fix.
docs: Changes that strictly affect documentation (e.g., README files).
refactor: Code changes that neither fix a bug nor add a feature.
test: Adding or correcting tests.
style: Changes that do not affect the meaning of the code (formatting, white-space, missing semicolons).chore: Updating build processes, auxiliary tools, or dependencies.
perf: Code changes that improve performance.
ci: Changes in the continuous integration or deployment setup.