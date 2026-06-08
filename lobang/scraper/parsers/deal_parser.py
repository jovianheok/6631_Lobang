from __future__ import annotations
# Allows type hints to be evaluated lazily as strings.
# This improves compatibility with forward references and reduces import issues.

import re
# Python's regular expression module used for pattern matching and text extraction.

from typing import Any, Optional
# Any: represents any data type.
# Optional[T]: indicates a value may either be type T or None.


# Keywords and phrases that strongly suggest the post is about food, deals, or promotions.
FOOD_POSITIVE_PATTERNS = [
    """
    r"": raw string
    \b...\b: word boundary
    \d: a digit
    \d+: one or more digits
    \s: any whitespace character
    \s: zero or 1 whitespace character
    \s*: zero or more whitespace characters
    [ -]?: either a space or a hyphen
    """

    r"\bfood\b",
    r"\bdeal(s)?\b",                    # matches: [deal, deals]
    r"\bpromo(tion)?\b",
    r"\boffer(s)?\b",
    r"\bdiscount(s)?\b",
    r"\bsale\b",
    r"\bvoucher(s)?\b",
    r"\bcoupon(s)?\b",
    r"\b1\s*[- ]?\s*for\s*[- ]?\s*1\b", # matches: [1 for 1, 1-for-1, 1 for-1 etc]
    r"\bbuy\s*1\s*free\s*1\b",
    r"\bb1f1\b",
    r"\bfree\s*1\b",                    # matches: [free 1, free1]
    r"\bbuffet\b",
    r"\bset\s*(meal|lunch|dinner)\b",   # matches: [set meal, set lunch, set dinner]
    r"\bmeal\b",
    r"\blunch\b",
    r"\bdinner\b",
    r"\bbreakfast\b",
    r"\bcafe\b",
    r"\brestaurant\b",
    r"\bhawker\b",
    r"\bkopitiam\b",
    r"\bcoffee\b",
    r"\bkopi\b",
    r"\btea\b",
    r"\bboba\b",
    r"\bbubble tea\b",
    r"\bburger\b",
    r"\bpizza\b",
    r"\bramen\b",
    r"\bsushi\b",
    r"\bnoodle(s)?\b",
    r"\bchicken rice\b",
    r"\bcai png\b",
    r"\bdessert\b",
    r"\bice cream\b",
    r"\bcinnamon\b",
]

# Terms that suggest the post is not a food deal, but instead a community/event-style post.
FOOD_NEGATIVE_PATTERNS = [
    r"\bcommunity\b",
    r"\bevent(s)?\b",
    r"\bneighbourhood\b",
    r"\bneighborhood\b",
    r"\bgroup(s)?\b",
    r"\brescue\b",
    r"\bshoutout\b",
    r"\brecommendation(s)?\b",
    r"\bplaces\b",
    r"\bjobs?\b",
    r"\bhousing\b",
    r"\bschool(s)?\b",
    r"\bworkshop(s)?\b",
    r"\bconcert(s)?\b",
]

# Generic words that should not be treated as merchant names.
MERCHANT_STOPWORDS = {
    "promo",
    "promotion",
    "deal",
    "deals",
    "offer",
    "offers",
    "discount",
    "sale",
    "limited",
    "time",
    "new",
    "best",
    "food",
    "finds",
}

# Patterns for extracting price-related text from a post.
PRICE_PATTERNS = [
    """
    ?:: non-capturing group
    |: 
    \$: literal dollar sign
    \d{1,2}: a digit repeated between 1 and 2 times, equivalent to any number 0 to 99
    """
    r"(?:S\$|\$)\s?\d+(?:\.\d{1,2})?",                      # matches: [$5, $12.50, S$8]
    r"\b\d+\s*for\s*(?:S\$|\$)?\s?\d+(?:\.\d{1,2})?\b",     # matches: [2 for $10, 3 for 5, 5 for S$12.90]
    r"\b\d+\s*[- ]?\s*for\s*[- ]?\s*\d+\b",
    r"\bbuy\s*1\s*free\s*1\b",
    r"\b1\s*[- ]?\s*for\s*[- ]?\s*1\b",
    r"\bfree\b",
]

# Patterns for extracting expiry / validity dates from the post.
DATE_PATTERNS = [
    r"\b\d{1,2}\s+[A-Z][a-z]{2,8}(?:\s*[-–to]+\s*\d{1,2}\s+[A-Z][a-z]{2,8})?\b",
    r"\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b",
    r"\b(?:until|till|til|ends?|valid\s*until)\s+\d{1,2}\s+[A-Z][a-z]{2,8}\b",
]

# Heuristics for spotting a location or outlet mention.
LOCATION_HINTS = [
    r"\ball outlets\b",
    r"\bselected outlets\b",
    r"\boutlets?\b",
    r"\bat\s+[A-Z][A-Za-z0-9&'().,-]{2,}",
    r"\bfrom\s+[A-Z][A-Za-z0-9&'().,-]{2,}",
    r"\bavailable\s+at\s+[A-Z][A-Za-z0-9&'().,-]{2,}",
]

# Words that indicate the post is explicitly verified or official.
VERIFIED_PATTERNS = [
    r"\bverified\b",
    r"\bofficial\b",
    r"\bconfirmed\b",
]

def parse_raw_post(raw_post: dict) -> Optional[dict]:
    """
    Main entry point for parsing a raw social media or scraped post.

    Workflow:
    1. Normalize the text content.
    2. Determine whether the post is a food deal.
    3. Extract structured information such as:
       - title
       - merchant name
       - price information
       - expiry date
       - location
       - verification status
    4. Return the extracted information as a standardized dictionary.

    Returns:
        dict containing extracted deal information if the post is valid.
        None if the post is empty or not classified as a food deal.
    """

    # Normalize the text first so downstream regex matching is more reliable.
    text = normalize_text(raw_post.get("text", ""))
    if not text:
        return None
    
    # Skip posts that do not look like food deals.
    if not is_food_deal(text):
        return None
    
    # Split into non-empty lines for title extraction.
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Extract the key structured fields from the post.
    title = extract_title(lines, text)
    merchant_name = extract_merchant_name(text, title)
    price_text = extract_first_match(text, PRICE_PATTERNS)
    expiry = extract_first_match(text, DATE_PATTERNS)
    location = extract_location(text)
    verification_status = extract_verification_status(text)

    return {
        "is_food_deal": True,
        "title": title,
        "merchant_name": merchant_name,
        "price_text": price_text,
        "location": location,
        "expiry_text": expiry,
        "verification_status": verification_status,
        "description": text,
        "source_url": raw_post.get("post_url") or raw_post.get("source_url"),
        "posted_at": raw_post.get("posted_at"),
        "content_hash": raw_post.get("content_hash"),
    }

def normalize_text(text: str) -> str:
    """
    Cleans and standardizes text before processing.

    Operations:
    - Converts different line-ending formats into '\n'
    - Removes excessive spaces and tabs
    - Reduces multiple blank lines
    - Trims leading and trailing whitespace

    Returns:
        Cleaned text string.
    """

    # Ensure text is never None, and standardize all line endings to '\n'.
    # Converting everything to '\n' makes later processing consistent.
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")

    # Replace runs of spaces and tabs with a single space.
    # This reduces formatting noise while preserving word separation.
    text = re.sub(r"[ \t]+", " ", text)

    # Replace 3 or more consecutive newlines with exactly 2 newlines.
    # Keeps paragraph breaks but removes excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove whitespace at the beginning and end of the text.
    # Prevents accidental leading/trailing spaces from affecting comparisons.
    return text.strip()

def is_food_deal(text: str) -> bool:
    """
    Determines whether a post likely describes a food-related promotion.

    Method:
    - Counts matches against positive food/deal keywords.
    - Counts matches against negative community/event keywords.
    - Rejects posts with strong non-deal signals.
    - Accepts posts containing at least one food/deal signal.

    Returns:
        True if the post is classified as a food deal.
        False otherwise.
    """

    # Convert the text to lowercase so matching is consistent.
    # This reduces dependence on capitalization.
    lowered = text.lower()

    # Count how many positive food/deal patterns appear.
    positive_hits = sum(
        1 for pattern in FOOD_POSITIVE_PATTERNS
        if re.search(pattern, lowered, flags=re.IGNORECASE)
    )

    # Count how many negative/non-deal patterns appear.
    negative_hits = sum(
        1 for pattern in FOOD_NEGATIVE_PATTERNS
        if re.search(pattern, lowered, flags=re.IGNORECASE)
    )

    # Reject posts that strongly look like non-deal content.
    if negative_hits >= 2 and positive_hits == 0:
        return False
    
    # Accept posts if at least one positive deal signal exists.
    if positive_hits >= 1:
        return True
    
    # Default case: No strong deal indicators were found.
    return False

def extract_title(lines: list[str], text: str) -> str:
    """
    Extracts a suitable title for the deal.

    Strategy:
    - Uses the first non-empty line when it is reasonably short.
    - Falls back to the first line of text if necessary.

    Returns:
        Title string.
    """

    # If there are no lines at all, we cannot extract a title.
    # Return an empty string instead of raising an error.
    if not lines:
        return ""
    
    # Take the first line and removes extra spaces, tabs, unwanted characters.
    first = clean_line(lines[0])

    # If the first line is reasonably short (length limit of 120 characters), assume it is the title.
    if len(first) <= 120:
        return first
    
    # If the first line is too long, truncate the first 120 characters (need to work on)
    return clean_line(text.split("\n", 1)[0])[:120]

def extract_merchant_name(text: str, fallback_title: str) -> str:
    candidates = []

    # Use the fallback title as the main string to inspect, and trim surrounding whitespace.
    title = fallback_title.strip()

    # If we have a non-empty title, store it as a candidate.
    if title:
        candidates.append(title)

    # Match a merchant name before a separator
    # Detect explicit @handles anywhere in the text
    # Detect attribution phrases like "by MerchantName"
    #
    #
    



def extract_first_match(text: str, patterns: list[str]) -> Optional[str]:
    """
    Searches a piece of text using a list of regular expressions.

    The first successful match is returned.

    Used for extracting:
    - prices
    - dates
    - other structured fields

    Returns:
        Matched text or None.
    """

def extract_location(text: str) -> Optional[str]:
    """
    Extracts outlet or location information from the post.

    Examples:
    - All outlets
    - Selected outlets
    - Available at Plaza Singapura

    Returns:
        Location string if found.
        None otherwise.
    """

def extract_verification_status(text: str) -> str:
    """
    Determines whether the post contains verification indicators.

    Looks for words such as:
    - verified
    - official
    - confirmed

    Returns:
        'verified' if a verification signal exists.
        'unknown' otherwise.
    """

def contains_food_signal(text: str) -> bool:
    """
    Checks whether text contains any known food or deal keywords.

    Used as a helper function during merchant extraction
    and food deal classification.

    Returns:
        True if a food-related keyword is found.
        False otherwise.
    """

def clean_line(value: str) -> str:
    """
    Normalizes a line of text.

    Operations:
    - Collapses repeated whitespace
    - Removes leading and trailing punctuation
    - Produces cleaner titles and extracted values

    Returns:
        Cleaned string.
    """

    # Replace any sequence of whitespace characters with a single space.
    value = re.sub(r"\s+", " ", (value or "").strip())

    # Remove common title separators and punctuation from both ends.
    value = value.strip(" -–—:|•·,")

    return value

def clean_merchant_candidate(value: str) -> str:
    """
    Cleans a potential merchant name.

    Operations:
    - Normalizes whitespace
    - Removes generic promotional words
      (e.g. deal, promo, offer)

    Returns:
        Refined merchant name candidate.
    """
    value = clean_line(value)

    # Remove any words that appear in MERCHANT_STOPWORDS.
    value = re.sub(r"\b(" + "|".join(MERCHANT_STOPWORDS) + r")\b", "", value, flags=re.IGNORECASE)

    # Collapse multiple spaces into one and trim surrounding whitespace.
    value = re.sub(r"\s{2,}", " ", value).strip()

    return value

def is_generic_merchant(value: str) -> bool:
    """
    Determines whether a merchant candidate is too generic
    to represent an actual business.

    Examples:
    - deal
    - promo
    - offer
    - food

    Returns:
        True if the value is generic.
        False otherwise.
    """
    lowered = value.lower()
    return lowered in {"deal", "deals", "promo", "promotion", "offer", "offers", "food", "finds"}
