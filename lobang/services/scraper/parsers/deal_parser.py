from __future__ import annotations              # Import annotations
#                                                 to refer to classes or types that do not exist yet

import re                                       # Import Python’s regular expression module 
#                                                 to search, match, split, or replace text patterns.

# Parse raw posts to extract title and merchant name
def parse_raw_post(raw_post: dict) -> dict:
    text = raw_post.get("text", "").strip()     # Get the "text" field and remove whitespace at the start and end
    lines = [line.strip() for line in text.splitlines() if line.strip()]    # Split text into lines. Trim whitespace
#                                                                             Remove empty lines
    title = lines[0][:100] if lines else ""     # Take the first line and limit it to 100 characters
    merchant_name = extract_merchant_name(text, title)

    return {
        "title": title,
        "merchant_name": merchant_name,
        "description": text,
        "source_url": raw_post.get("post_url") or raw_post.get("source_url"),
        "content_hash": raw_post.get("content_hash"),
    }

# Extract merchant name by removing common promo words and trailing emoji/punctuation noise
def extract_merchant_name(text: str, fallback_title: str) -> str:
    candidate = fallback_title.strip()
    
    candidate = re.sub(                     # Syntax: re.sub(pattern, replacement, text)
        r"\b(promo|promotion|deal|offers?|discount|sale|limited time)\b",
        "",
        candidate,
        flags=re.IGNORECASE,
    )
    candidate = re.sub(
        r"[^\w&'’().,-]+",                  # Replace characters that are NOT \w&'’().,-]+
        " ",
        candidate).strip()
    
    candidate = re.sub(
        r"\s{2,}",                          # Replace two or more whitespaces
        " ", 
        candidate).strip()
    
    return candidate or fallback_title[:100] # Return candidate if it is not empty else fallback_title