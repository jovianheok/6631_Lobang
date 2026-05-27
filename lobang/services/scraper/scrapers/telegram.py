from playwright.sync_api import sync_playwright             # Import Playwright so we can control a browser synchronously
import hashlib                                              # Import Python’s hashing library to create a unique fingerprint for each post

CHANNEL_URL = "https://t.me/s/sgfooddeals"                  # Telegram channel page that we want to scrape

# Create a unique hash from post text and post URL
def make_content_hash(text: str, post_url: str) -> str:
    base = f"{post_url}|{text.strip()}"                     # Combine the URL and cleaned text into one string
    return hashlib.sha256(base.encode("utf-8")).hexdigest() # Convert string into a SHA-256 hash and return it as a hex string

# Use Playwright to scrape text posts from a Telegram channel and return them as a list of structured dictionaries
def scrape_telegram_channel():
    raw_posts = []
    
    with sync_playwright() as p:                            # Open a Playwright session and cleans it up automatically afterward
        browser = None

        try:
            browser = p.chromium.launch(headless=True)         # Launch a Chromium browser in background
            page = browser.new_page()                           # Create a new browser tab
            page.goto(CHANNEL_URL, wait_until="networkidle")    # Load the Telegram channel page and wait until network activity becomes minimal
            page.wait_for_timeout(2000)                         # Give dynamic content more time to render

            posts = page.locator("div.tgme_widget_message")     # Find all Telegram post elements on the page

            count = posts.count()
            for i in range(count):                             # Loop through every post using its index
                post = posts.nth(i)                            # Get the i-th post from the locator collection

                text_locator = post.locator(".tgme_widget_message_text")    # Find the element containing the message text
                date_locator = post.locator("a.tgme_widget_message_date")   # Finds the anchor (<a>) element containing the post date

                text = text_locator.inner_text().strip() if text_locator.count() else "" 
                # Check if the text element exist. If yes: Extract visible text and remove extra spaces/newlines

                post_url = date_locator.get_attribute("href") if date_locator.count() else None     
                # Check if the date link exists. If yes: Get the href attribute (URL)

                posted_at = date_locator.inner_text().strip() if date_locator.count() else None

                if not text:                                   # Skip posts with empty text
                    continue
                
                raw_posts.append({
                    "source_url": CHANNEL_URL,
                    "post_url": post_url,
                    "posted_at": posted_at,
                    "text": text,
                    "content_hash": make_content_hash(text, post_url),
                })

        finally:                                                    # So that browser still closes if scraping fails
            if browser:
                browser.close()                                     # Shuts the browser down

    return raw_posts
    