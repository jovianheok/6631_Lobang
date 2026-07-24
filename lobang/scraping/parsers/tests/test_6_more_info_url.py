import pytest

from ..deal_parser import parse_raw_post
from .testcases import TEST_CASES


@pytest.mark.parametrize(
    "case",
    TEST_CASES,
)
def test_parse_raw_post_more_info_url(case: dict):
    result = parse_raw_post(case)
    if case["expected"]["is_food_deal"]:
        assert result["more_info_url"] == case["expected"].get("more_info_url")
