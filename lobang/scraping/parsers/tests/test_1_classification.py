import pytest
from ..deal_parser import parse_raw_post
from .testcases import TEST_CASES

@pytest.mark.parametrize(       # decorator
    "case",
    TEST_CASES,
)
def test_parse_raw_post(case):
    result = parse_raw_post(case)

    # Food deals
    if case["expected"]["is_food_deal"]:
        assert result is not None
    
    # Non-food deals
    else:
        assert result is None