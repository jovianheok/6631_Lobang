"""
Purpose: Turn a webpage into a list of Python dictionaries which stores raw posts
"""

import hashlib      # import Python’s hashing library to create a unique fingerprint for each post
from urllib.parse import urlparse

from playwright.sync_api import Locator, sync_playwright     # import Playwright to control a browser synchronously

from .image_utils import extract_background_image_url

CHANNEL_URL = "https://t.me/s/sgfooddeals"      # Telegram channel page that we want to scrape          
MAX_POSTS = 50
SCROLL_STEP_PX = 5000
SCROLL_WAIT_MS = 1200
MAX_STABLE_SCROLLS = 3


def _read_photo_locator(photo_locator: Locator) -> str | None:
    """
    Read the best available image URL from a Telegram photo wrapper.
    """
    photo_style = photo_locator.get_attribute("style")
    image_url = extract_background_image_url(photo_style)
    if image_url:
        return image_url

    img_locator = photo_locator.locator("img").first
    if img_locator.count():
        for attr in ("src", "data-src"):
            candidate = img_locator.get_attribute(attr)
            if candidate:
                return candidate.strip()

    return None


def extract_post_image_url(post: Locator) -> str | None:
    """
    Purpose: Extract the most likely image URL from a Telegram post.
    """
    photo_locator = post.locator(".tgme_widget_message_photo_wrap").first
    if not photo_locator.count():
        return None

    return _read_photo_locator(photo_locator)


def extract_post_id(post_url: str | None) -> int:
    """
    Purpose: Extract Telegram's numeric message id from a post URL.
    """
    if not post_url:
        return -1

    path_parts = [part for part in urlparse(post_url).path.split("/") if part]
    if not path_parts:
        return -1

    try:
        return int(path_parts[-1])
    except ValueError:
        return -1


def load_more_posts(page, posts: Locator, max_posts: int):
    """
    Purpose: Scroll until Telegram has loaded enough posts or stops loading more.
    """
    stable_scrolls = 0
    previous_count = posts.count()

    while previous_count < max_posts and stable_scrolls < MAX_STABLE_SCROLLS:
        page.mouse.wheel(0, SCROLL_STEP_PX)
        page.wait_for_timeout(SCROLL_WAIT_MS)

        current_count = posts.count()
        if current_count > previous_count:
            previous_count = current_count
            stable_scrolls = 0
            continue

        stable_scrolls += 1


def make_content_hash(text: str, post_url: str) -> str:
    """
    Purpose: Create a unique hash from post text and post URL to detect duplicate posts
    """
    base = f"{post_url}|{text.strip()}" # Combine URL and cleaned text into one string
    return hashlib.sha256(base.encode("utf-8")).hexdigest()     # Convert string into a SHA-256 hash and return it as a hex string


def scrape_telegram_channel(max_posts: int = MAX_POSTS):
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
            load_more_posts(page, posts, max_posts)
            
            count = posts.count()
            for i in range(count):                             
                post = posts.nth(i)                           
                text_locator = post.locator(".tgme_widget_message_text")        # Find the text element
                date_locator = post.locator("a.tgme_widget_message_date")       # Find the date element

                # Telegram lazily loads media for off-screen posts, so scroll each
                # card into view before reading photo attributes.
                post.scroll_into_view_if_needed()
                page.wait_for_timeout(150)

                text = text_locator.inner_text().strip() if text_locator.count() else ""        # Extract text and remove extra spaces/newlines if text element exists
                
                post_url = date_locator.get_attribute("href") if date_locator.count() else None     # Extract URL and date if date element exists
                time_posted = date_locator.inner_text().strip() if date_locator.count() else None
                image_url = extract_post_image_url(post)

                if not text:        # Skip posts with empty text                        
                    continue
                
                raw_posts.append({
                    "source_url": CHANNEL_URL,
                    "post_url": post_url,
                    "posted_at": time_posted,
                    "text": text,
                    "image_url": image_url,
                    "content_hash": make_content_hash(text, post_url),
                })

            raw_posts.sort(key=lambda post: extract_post_id(post.get("post_url")), reverse=True)
            raw_posts = raw_posts[:max_posts]

        finally:                                                    
            if browser:
                browser.close()                                     

    return raw_posts
    
