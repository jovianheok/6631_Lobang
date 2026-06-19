"""
Purpose: Coordinate the pipeline: scrape -> store -> parse -> enrich -> store
"""

from scrapers.telegram import scrape_telegram_channel
from parsers.deal_parser import parse_raw_post
from database.storage import save_raw_posts, save_parsed_deals
from googleplaces.enricher import enrich_merchant

def main():
    try:
        raw_posts = scrape_telegram_channel()                                       # Scrape telegram channel
        print(f"Scraped {len(raw_posts)} posts")

        inserted_raw_post_ids = save_raw_posts(raw_posts, source_id=1)              # Save raw posts to database
        print(f"Inserted {len(inserted_raw_post_ids)} new raw posts")

        parsed_deals = []
        for post in raw_posts:
            deal = parse_raw_post(post)
            if deal is None:
                continue

            merchant_name = deal.get("merchant_name")
            if merchant_name:
                places_data = enrich_merchant(merchant_name)
                if places_data:
                    deal.update(places_data)

            parsed_deals.append(deal)

        inserted_parsed_deal_ids = save_parsed_deals(parsed_deals, source_id=1)    # Save parsed deals to database
        print(f"Inserted {len(inserted_parsed_deal_ids)} parsed deals")

    except Exception as e:
        print("Pipeline failed: ")
        print(e)


if __name__ == "__main__":
    main()
