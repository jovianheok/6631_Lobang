import pytest
from ..deal_parser import parse_raw_post
from .testcases import TEST_CASES

@pytest.mark.parametrize(
    "case",
    TEST_CASES,
)
def test_parse_raw_post(case):
    result = parse_raw_post({"text": case["text"]})
    if case["expected"]["is_food_deal"]:
        assert result["merchant_name"] == case["expected"]["merchant_name"]