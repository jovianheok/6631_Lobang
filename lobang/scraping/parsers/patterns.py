"""
Purpose: Central store for regex patterns and shared constants
"""

r"""
r"..."  : raw string literal
\b      : word boundary
\d      : a digit
\d+     : one or more digits
\s      : a whitespace character
\s+     : one or more whitespace character
\s?     : zero or one whitespace character
\s*     : zero or more whitespace characters
[ -]?   : an optional space or hyphen
^:      : matches the start of the string (leading)
$       : matches the end of the string (trailing)
"""

# _1_classification.py
FOOD_PATTERNS = [
    # Generic food terms
    r"\bfood\b", r"\bmeal(s)?\b", r"\blunch\b", r"\bdinner\b", r"\bbreakfast\b", r"\bbuffet\b", r"\bdining\b",

    # Drinks
    r"\bcoffee\b", r"\btea\b", r"\bboba\b", r"\bbubble tea\b", r"\bdrink(s)?\b", r"\bfrappuccino(s)?\b", r"\brefreshers?\b",

    # Protein / mains
    r"\bchicken\b", r"\bbeef\b", r"\bpork\b", r"\bfish\b", r"\bseafood\b", r"\bburger(s)?\b", r"\bpizza(s)?\b", r"\bramen\b",
    r"\bsushi\b", r"\bnoodle(s)?\b", r"\bprawn(s)?\b", r"\bwing(s)?\b",

    # Desserts and snacks
    r"\bgelato\b", r"\bice cream\b", r"\bdessert(s)?\b", r"\bcake\b", r"\bcookie(s)?\b", r"\bdonut(s)?\b", r"\bmochi\b",
    r"\bkakigori\b", r"\bmatcha\b", r"\bsnack(s)?\b", r"\bchips?\b", r"\bcrisps?\b", r"\bpopcorn\b",

    # Broad restaurant menu categories
    r"\bbowl(s)?\b", r"\bcombo(s)?\b", r"\bset(s)?\b", r"\bplatter(s)?\b",

    # Food venues
    r"\bcafe\b", r"\bcafé\b", r"\brestaurant\b", r"\bbakery\b", r"\bhawker\b", r"\bkopitiam\b",

    # Convenience store
    r"\bready[- ]to[- ]go\b", r"\bready[- ]to[- ]eat\b", r"\bhotdog(s)?\b", r"\bsandwich(es)?\b", r"\bwrap(s)?\b", r"\bonigiri\b",
    r"\brice ball(s)?\b", r"\bbento\b", r"\bmeal box(es)?\b", 
    
    # Bakery
    r"\bbun(s)?\b", r"\bpastr(y|ies)\b", r"\bcroissant(s)?\b", r"\bmuffin(s)?\b",
]

STRONG_DEAL_PATTERNS = [
    # 1-for-1 / BOGO
    r"\b1\s*[- ]?\s*for\s*[- ]?\s*1\b", r"\bbuy\s*1\s*get\s*1\b", r"\bbuy\s*1\s*free\s*1\b", r"\bb1f1\b",

    # Free
    r"\bfree\b", r"\bcomplimentary\b",

    # Percentage discount
    r"\b\d{1,3}%\s*off\b", r"\bup\s+to\s+\d{1,3}%\s*off\b",

    # Dollar discount
    r"\$(?:\d+(?:\.\d{1,2})?)\s*off\b",

    # Price-led offers
    r"(?:S\$|\$)\s?\d+(?:\.\d{1,2})?", r"\bonly\s+(?:S\$|\$)?\s?\d+(?:\.\d{1,2})?", r"\bfrom\s+(?:S\$|\$)?\s?\d+(?:\.\d{1,2})?",

    # Bundles / multi-buy
    r"\b\d+\s*for\s*(?:S\$|\$)?\s?\d+(?:\.\d{1,2})?\b",

    # Strong urgency
    r"\bwhile stocks? last\b", r"\bU\.P\.\s*\$?\d+(?:\.\d{1,2})?\b",
]

NEGATIVE_PATTERNS = [
    # Channel labels
    r"#shoutout\b", r"#article\b",

    # Editorial content
    r"\bguide\b", r"\bspot(s)?\b", r"\btelegram channel\b", r"\bbest spots\b", r"\bplaces to get\b",

    # Community content
    r"\bcommunity\b", r"\bfriend circle\b", r"\bmake new friends\b", r"\bmeetup(s)?\b", 

    # Events
    r"\bevent(s)?\b", r"\bworkshop(s)?\b",

    # Giveaways
    r"\bgiveaway\b", r"\bcontest\b", r"\blucky winner(s)?\b", r"\bwin\b", r"\bstand to win\b",
]

# _3_extract_merchant.py
GENERIC_PROMO_WORDS = {
    "promo", "promotion", "deal", "deals", "offer", "offers", "discount", "sale", "limited", "time", "new", "best", "food", "finds",
}

AT_PATTERNS = [
    r"\bback at\s+([A-Za-z0-9&'\- ]+)", r"\bavailable at\s+([A-Za-z0-9&'\- ]+)", r"\bonly at\s+([A-Za-z0-9&'\- ]+)",
    r"\bexclusively at\s+([A-Za-z0-9&'\- ]+)",
]

NON_MERCHANT_LOCATION_PHRASES = {
    "all outlets", "selected outlets", "participating outlets", "all stores",
    "selected stores", "participating stores", "all locations",
}

# _4_extract_validity.py
MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3, "apr": 4, "april": 4, "may": 5, 
    "jun": 6, "june": 6, "jul": 7, "july": 7, "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}

EXPIRY_KEYWORDS = [
    "now till", "till", "until", "ends", "end", "valid till", "available till", "giveaway ends", 
    "promotion ends", "deal ends",
]

# _5_extract_location.py
LOCATION_HINT_PATTERNS = [
    r"^📍\s*([^\n.,;]+)$", r"\blocation\s*[:\-]\s*([^\n.,;]+)", r"\blocations\s*[:\-]\s*([^\n.,;]+)",
    r"\bonly at\s+([^\n.,;]+)", r"\bavailable at\s+([^\n.,;]+)", r"\bback at\s+([^\n.,;]+)",
    r"\bexclusively at\s+([^\n.,;]+)",
]

# _6_extract_place_info.py
CUISINE_TYPE_MAP = {
    "chinese_restaurant": "Chinese", "japanese_restaurant": "Japanese", "korean_restaurant": "Korean",
    "indian_restaurant": "Indian", "thai_restaurant": "Thai", "italian_restaurant": "Italian",
    "american_restaurant": "American", "mexican_restaurant": "Mexican", "seafood_restaurant": "Seafood",
    "vegetarian_restaurant": "Vegetarian", "vegan_restaurant": "Vegan", "french_restaurant": "French",
    "mediterranean_restaurant": "Mediterranean", "middle_eastern_restaurant": "Middle Eastern",
    "vietnamese_restaurant": "Vietnamese", "indonesian_restaurant": "Indonesian",
    "malaysian_restaurant": "Malaysian", "ramen_restaurant": "Ramen", "sushi_restaurant": "Sushi",
    "pizza_restaurant": "Pizza", "hamburger_restaurant": "Burgers", "sandwich_shop": "Sandwiches",
    "bakery": "Bakery", "cafe": "Cafe", "bar": "Bar", "ice_cream_shop": "Ice Cream", 
    "bubble_tea_store": "Bubble Tea",
}

PRICE_LEVEL_MAP = {
    "PRICE_LEVEL_FREE": 0, "PRICE_LEVEL_INEXPENSIVE": 1, "PRICE_LEVEL_MODERATE": 2,
    "PRICE_LEVEL_EXPENSIVE": 3, "PRICE_LEVEL_VERY_EXPENSIVE": 4,
}

REGION_ORDER = ["north", "south", "east", "west", "central"]

REGION_KEYWORDS = {
    "north": ["woodlands", "yishun", "sembawang", "admiralty", "khatib", "springleaf", "marsiling",],
    "south": ["harbourfront", "sentosa", "telok blangah", "bukit merah", "keppel",],
    "east": ["tampines", "pasir ris", "bedok", "simei", "changi", "siglap", "marine parade",
                "katong", "joo chiat", "eunos",],
    "west": ["jurong", "clementi", "boon lay", "pioneer", "bukit batok", "choa chu kang",
                "bukit panjang", "west coast",],
    "central": ["orchard", "bugis", "dhoby ghaut", "novena", "bishan","toa payoh", "city hall",
                "raffles place", "tanjong pagar", "newton", "serangoon", "ang mo kio", "little india",
                "clarke quay", "marina bay",],
}

ISLANDWIDE_OUTLET_THRESHOLD = 20

# _7_resolve_location.py
EXPLICIT_LOCATION_PATTERNS = [
    r"\b(all outlets?(?:\s+except\s+[^\n.,;]+)?)\b", r"\b(selected outlets?(?:\s+only)?)\b",
    r"\b(participating outlets?(?:\s+only)?)\b", r"\b(all stores?(?:\s+except\s+[^\n.,;]+)?)\b",
    r"\b(selected stores?(?:\s+only)?)\b", r"\b(participating stores?(?:\s+only)?)\b",
    r"\b(all locations?(?:\s+except\s+[^\n.,;]+)?)\b", r"\b(selected locations?(?:\s+only)?)\b",
    r"\b(participating locations?(?:\s+only)?)\b",
]

# _8_extract_more_info_url.py
MORE_INFO_PATTERNS = [
    r"\b(?:find out more|more info|order here|join here)\b\s*[:\-]\s*(https?://\S+|tco\.sg/\S+)",
]
