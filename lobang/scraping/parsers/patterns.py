"""
Purpose: Store all regex patterns in one place so the parser logic stays clean
"""

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
# List of regular expression patterns to identify food-related terms.
FOOD_PATTERNS = [
    # Generic food terms
    r"\bfood\b",
    r"\bmeal(s)?\b",
    r"\blunch\b",
    r"\bdinner\b",
    r"\bbreakfast\b",
    r"\bbuffet\b",
    r"\bdining\b",

    # Drinks
    r"\bcoffee\b",
    r"\btea\b",
    r"\bboba\b",
    r"\bbubble tea\b",
    r"\bdrink(s)?\b",

    # Food categories
    r"\bburger(s)?\b",
    r"\bpizza\b",
    r"\bramen\b",
    r"\bsushi\b",
    r"\bnoodle(s)?\b",
    r"\bdonut(s)?\b",
    r"\bpretzel(s)?\b",
    r"\bacai\b",
    r"\bgelato\b",
    r"\bice cream\b",
    r"\bdessert(s)?\b",
    r"\bcake\b",
    r"\bcookie(s)?\b",

    # Food venues
    r"\bcafe\b",
    r"\bcafé\b",
    r"\brestaurant\b",
    r"\bbakery\b",
    r"\bhawker\b",
    r"\bkopitiam\b",
]

# List of regular expression patterns to identify promotions and discounts
DEAL_PATTERNS = [
    # 1-for-1 variants
    r"\b1\s*[- ]?\s*for\s*[- ]?\s*1\b",
    r"\bbuy\s*1\s*free\s*1\b",
    r"\bb1f1\b",

    # Generic deal words
    r"\bdeal(s)?\b",
    r"\boffer(s)?\b",
    r"\bpromo(s)?\b",
    r"\bpromotion(s)?\b",
    r"\bsale\b",
    r"\bvoucher(s)?\b",
    r"\bcoupon(s)?\b",

    # Free items
    r"\bfree\b",
    r"\bcomplimentary\b",

    # Percentage discounts
    r"\b\d{1,3}%\s*off\b",
    r"\bup\s+to\s+\d{1,3}%\s*off\b",

    # Dollar discounts
    r"\$(?:\d+(?:\.\d{1,2})?)\s*off\b",

    # Price-led deals
    r"(?:S\$|\$)\s?\d+(?:\.\d{1,2})?",
    r"\bonly\s+(?:S\$|\$)?\s?\d+(?:\.\d{1,2})?",
    r"\bfrom\s+(?:S\$|\$)?\s?\d+(?:\.\d{1,2})?",

    # Bundle deals
    r"\b\d+\s*for\s*(?:S\$|\$)?\s?\d+(?:\.\d{1,2})?\b",

    # Redemptions / perks
    r"\bredemption(s)?\b",
    r"\bperk(s)?\b",
]

# List of regular expression patterns to identify non-deal content
NEGATIVE_PATTERNS = [
    # Channel labels
    r"#shoutout\b",
    r"#article\b",

    # Editorial content
    r"\bguide\b",
    r"\bspot(s)?\b",
    r"\bplaces?\b",

    # Community content
    r"\bcommunity\b",
    r"\bfriend circle\b",
    r"\bmake new friends\b",
    r"\bmeetup(s)?\b",

    # Events
    r"\bevent(s)?\b",
    r"\bworkshop(s)?\b",

    # Giveaways
    r"\bgiveaway\b",
    r"\bcontest\b",
    r"\blucky winner(s)?\b",
]

# List of regular expression patterns to extract prices and discounts
PRICE_PATTERNS = 

# List of regular expression patterns to extract dates, validity and expiry
DATE_PATTERNS = 

# List of regular expression patterns to extract location
LOCATION_PATTERNS = 

# Set of generic promotional words that should not be treated as merchant names during extraction
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