# Lobang

Lobang is a food-deal discovery app that collects promotions from Telegram posts, turns them into structured deals, and shows them in a cleaner, easier-to-browse feed.

## Features

- Browse current food deals in one place.
- View deal details such as merchant, image, location, time validity, date validity, and source links.
- Open the original Telegram post or a parsed "more info" link when available.
- Save bookmarks for deals you want to revisit.
- Upvote and downvote deals so the community can surface better deals and suppress poor ones.
- Get a personalized "For You" feed based on your saved preferences.

## How To Use

1. Open the app and browse the latest active deals on the home page.
2. Open a deal card to review its details, including validity period, timing, location, and links.
3. Use the save button to bookmark deals you want to keep.
4. Sign in to vote on deals and improve community recommendations.
5. Update your preferences in your profile to personalize your "For You" feed.

## Running Locally

Run these commands from the `lobang/` directory.

### Frontend

```bash
cd apps/frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

### Backend

```bash
cd apps/backend
source .venv/bin/activate
uvicorn src.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

### Scraper

```bash
cd scraping
source .venv/bin/activate
python main.py
```

## Notes

- Some features, such as bookmarks, voting, and personalization, require signing in.
- Deals are scraped and parsed from external sources, so displayed information depends on what is available in the original post.
- For implementation details, see [docs/architecture.md](/Users/jovianheok/Desktop/orbital/6631_Lobang/lobang/docs/architecture.md).
