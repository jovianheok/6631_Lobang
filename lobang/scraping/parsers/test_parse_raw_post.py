import pytest
from deal_parser import parse_raw_post

TEST_CASES = [
    {
        "deal name": "valid_food_deal_1",
        "text": "Auntie Anne's: 1-for-1 Cinnamon Sugar Pretzel 🥨",
        "expected": {
            "is_food_deal": True,
            "title": "Auntie Anne's: 1-for-1 Cinnamon Sugar Pretzel",
            "merchant_name": "Auntie Anne's",
        },
    },
    {
        "deal name": "valid_food_deal_2",
        "text": "KFC: 1-for-1 Chicken Tender 🍗",
        "expected": {
            "is_food_deal": True,
            "title": "KFC: 1-for-1 Chicken Tender",
            "merchant_name": "KFC",
        },
    },
    {
        "deal name": "valid_food_deal_3",
        "text": "Texas Chicken: 5-pc Drumlets for $5 🍗",
        "expected": {
            "is_food_deal": True,
            "title": "Texas Chicken: 5-pc Drumlets for $5",
            "merchant_name": "Texas Chicken",
        },
    },
    {
        "deal name": "non_food_deal_1",
        "text": "SG Friend Up: New Friend Circle Starts Here 👋",
        "expected": {
            "is_food_deal": False,
        },
    },
]

@pytest.mark.parametrize(       # decorator
    "case",
    TEST_CASES,
    ids=[c["deal name"] for c in TEST_CASES]        # Give each test run a readable name in pytest output
)
def test_parse_raw_post(case):
    result = parse_raw_post({"text": case["text"]})      # Create an input dictionary and pass to parse_raw_post as required

    # Food deals
    if case["expected"]["is_food_deal"]:
        assert result is not None
        assert result["title"] == case["expected"]["title"]
        assert result["merchant_name"] == case["expected"]["merchant_name"]
    
    # Non-food deals
    else:
        assert result is None