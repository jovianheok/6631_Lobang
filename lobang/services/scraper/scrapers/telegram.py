# Import Playwright so we can control a browser synchronously
from playwright.sync_api import sync_playwright

# Import Python’s hashing library to create a unique fingerprint for each post
import hashlib

# Telegram channel page that we want to scrape
CHANNEL_URL = "https://t.me/s/sgfooddeals"                  

# Create a unique hash from post text and post URL
def make_content_hash(text: str, post_url: str) -> str:

    # Combine the URL and cleaned text into one string
    base = f"{post_url}|{text.strip()}"

    # Convert string into a SHA-256 hash and return it as a hex string
    return hashlib.sha256(base.encode("utf-8")).hexdigest() 

# Use Playwright to scrape text posts from a Telegram channel and return them as a list of structured dictionaries
def scrape_telegram_channel():
    raw_posts = []
    
    # Open a Playwright session and cleans it up automatically afterward
    with sync_playwright() as p:
        browser = None

        try:
            # Launch a Chromium browser in background
            browser = p.chromium.launch(headless=True)

            # Create a new browser tab
            page = browser.new_page()
            
            # Load the Telegram channel page and wait until network activity becomes minimal
            page.goto(CHANNEL_URL, wait_until="networkidle")

            # Give dynamic content more time to render
            page.wait_for_timeout(2000)

            # Find all Telegram post elements on the page
            posts = page.locator("div.tgme_widget_message")

            count = posts.count()
            # Loop through every post using its index
            for i in range(count):                             
                # Get the i-th post from the locator collection
                post = posts.nth(i)                           

                # Find the element containing the message text
                text_locator = post.locator(".tgme_widget_message_text")    

                # Finds the anchor (<a>) element containing the post date
                date_locator = post.locator("a.tgme_widget_message_date")

                # Check if the text element exist. If yes: Extract visible text and remove extra spaces/newlines
                text = text_locator.inner_text().strip() if text_locator.count() else "" 

                # Check if the date link exists. If yes: Get the href attribute (URL)
                post_url = date_locator.get_attribute("href") if date_locator.count() else None     
                
                posted_at = date_locator.inner_text().strip() if date_locator.count() else None

                # Skip posts with empty text
                if not text:                                   
                    continue
                
                raw_posts.append({
                    "source_url": CHANNEL_URL,
                    "post_url": post_url,
                    "posted_at": posted_at,
                    "text": text,
                    "content_hash": make_content_hash(text, post_url),
                })

        # So that browser still closes if scraping fails
        finally:                                                    
            if browser:
                # Shuts the browser down
                browser.close()                                     

    return raw_posts
    