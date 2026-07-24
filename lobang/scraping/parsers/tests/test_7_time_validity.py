import pytest

from ..deal_parser import parse_raw_post
from .testcases import TEST_CASES


@pytest.mark.parametrize(
    "case",
    TEST_CASES,
)
def test_parse_raw_post_time_and_validity(case: dict):
    result = parse_raw_post(case)
    if case["expected"]["is_food_deal"]:
        assert result["time_text"] == case["expected"].get("time_text")
