"""
Purpose: Store all regex patterns in one place so the parser logic stays clean
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

# _3_merchant.py
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

# List of regular expression patterns to extract dates, validity and expiry
# DATE_PATTERNS = 

# List of regular expression patterns to extract location
# LOCATION_PATTERNS = 

# Set of generic promotional words that should not be treated as merchant names during extraction

# 
