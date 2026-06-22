"""
Purpose: Turn a webpage into a list of Python dictionaries which stores raw posts
"""

from playwright.sync_api import sync_playwright     # import Playwright to control a browser synchronously

import hashlib      # import Python’s hashing library to create a unique fingerprint for each post

CHANNEL_URL = "https://t.me/s/sgfooddeals"      # Telegram channel page that we want to scrape          

def make_content_hash(text: str, post_url: str) -> str:
    """
    Purpose: Create a unique hash from post text and post URL to detect duplicate posts
    """
    base = f"{post_url}|{text.strip()}" # Combine URL and cleaned text into one string
    return hashlib.sha256(base.encode("utf-8")).hexdigest()     # Convert string into a SHA-256 hash and return it as a hex string


def scrape_telegram_channel():
    """
    Use Playwright to scrape text posts from a Telegram channel and return them as a list of structured dictionaries
    # """
    raw_posts = []
    
    with sync_playwright() as p:        # Open a Playwright session and clean up automatically afterward
        browser = None      # Declare the variable before it is assigned

        try:
            browser = p.chromium.launch(headless=True)      # Launch a Chromium browser in background
            page = browser.new_page()       # Create a new browser tab
            page.goto(CHANNEL_URL, wait_until="networkidle")        # Load the Telegram channel page and wait until network activity becomes minimal
            page.wait_for_timeout(2000)     # Give dynamic content more time to render

            posts = page.locator("div.tgme_widget_message")     # Find all Telegram post elements on the page
            
            count = posts.count()
            for i in range(count):                             
                post = posts.nth(i)                           
                text_locator = post.locator(".tgme_widget_message_text")        # Find the text element
                date_locator = post.locator("a.tgme_widget_message_date")       # Find the date element

                text = text_locator.inner_text().strip() if text_locator.count() else ""        # Extract text and remove extra spaces/newlines if text element exists
                
                post_url = date_locator.get_attribute("href") if date_locator.count() else None     # Extract URL and date if date element exists
                time_posted = date_locator.inner_text().strip() if date_locator.count() else None

                if not text:        # Skip posts with empty text                        
                    continue
                
                raw_posts.append({
                    "source_url": CHANNEL_URL,
                    "post_url": post_url,
                    "posted_at": time_posted,
                    "text": text,
                    "content_hash": make_content_hash(text, post_url),
                })

        finally:                                                    
            if browser:
                browser.close()                                     

    return raw_posts
    