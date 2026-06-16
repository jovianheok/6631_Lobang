import pytest
from deal_parser import parse_raw_post

TEST_CASES = [
    {
        "name": "auntie_annes_1for1",
        "text": "Auntie Anne’s: 1-for-1 Cinnamon Sugar Pretzel 🥨",
        "expected": {
            "is_food_deal": True,
            "merchant_name": "Auntie Anne's",
        },
    },
    {
        "name": "kfc_1for1",
        "text": "KFC: 1-for-1 Finger Licking Deals 🍗",
        "expected": {
            "is_food_deal": True,
            "merchant_name": "KFC",
        },
    },
    {
        "name": "texas_chicken_5_dollar",
        "text": "Texas Chicken: 5-pc Drumlets for $5 🍗",
        "expected": {
            "is_food_deal": True,
            "merchant_name": "Texas Chicken",
        },
    },
    {
        "name": "starbucks_1for1",
        "text": "Starbucks: 1-for-1 on any Venti drink 🥤",
        "expected": {
            "is_food_deal": True,
            "merchant_name": "Starbucks",
        },
    },
    {
        "name": "vietnamese_coffee_shoutout",
        "text": "5 Vietnamese Salt Coffee Spots in SG 🥤",
        "expected": {
            "is_food_deal": False,
        },
    },
    {
        "name": "gastrobeats_food_guide",
        "text": "GastroBeats 2026 Food Guide 🍩",
        "expected": {
            "is_food_deal": False,
        },
    },
    {
        "name": "sg_friend_up",
        "text": "SG Friend Up: New Friend Circle Starts Here 👋",
        "expected": {
            "is_food_deal": False,
        },
    },
]

@pytest.mark.parametrize("case", TEST_CASES, ids=[c["name"] for c in TEST_CASES])
def test_parse_raw_post(case):
    result = parse_raw_post(case["text"])

    for key, expected_value in case["expected"].items():
        assert result[key] == expected_value, f"{case['name']} failed on {key}"