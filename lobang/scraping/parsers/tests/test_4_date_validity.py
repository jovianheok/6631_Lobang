import pytest
from ..deal_parser import parse_raw_post
from .testcases import TEST_CASES

@pytest.mark.parametrize(
    "case",
    TEST_CASES,
)
def test_parse_raw_post_date_validity(case: dict):
    result = parse_raw_post(case)
    if case["expected"]["is_food_deal"]:
        assert result["start_date"] == case["expected"]["start_date"]
        assert result["end_date"] == case["expected"]["end_date"]
