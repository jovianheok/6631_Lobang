from scrapers.telegram import scrape_telegram_channel
from db.storage import save_raw_posts
from parsers.deal_parser import parse_raw_post

def main():
    try:
        raw_posts = scrape_telegram_channel()                   # Scrape telegram channel
        print(f"Scraped {len(raw_posts)} posts")

        inserted_ids = save_raw_posts(raw_posts, source_id=1)   # Save raw posts to database
        print(f"Inserted {len(inserted_ids)} new raw posts")

        parsed_deals = [parse_raw_post(post) for post in raw_posts] # Parse raw posts
        print("Sample parsed deals:")
        for deal in parsed_deals[:5]:
            print(deal)

    except Exception as e:
        print("Pipeline failed: ")
        print(e)


if __name__ == "__main__":
    main()

