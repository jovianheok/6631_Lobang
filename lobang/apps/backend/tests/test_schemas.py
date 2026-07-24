"""
Schema-level unit tests. No app, DB, or network needed.
"""

from datetime import date

import pytest
from pydantic import ValidationError

from src.schemas.deal_schema import DealOut
from src.schemas.submission_schema import SubmissionIn


# --- DealOut: date handling (regression guard for commit 98b03e3) ---

def test_dealout_accepts_date_object_from_db():
    # psycopg2 returns DATE columns as datetime.date; DealOut must accept it.
    deal = DealOut(id=1, title="X", start_date=date(2026, 7, 31))
    assert deal.start_date == date(2026, 7, 31)


def test_dealout_serializes_date_to_iso_string():
    deal = DealOut(
        id=1, title="X", start_date=date(2026, 7, 31), end_date=date(2026, 8, 1)
    )
    dumped = deal.model_dump(mode="json")
    assert dumped["start_date"] == "2026-07-31"
    assert dumped["end_date"] == "2026-08-01"


def test_dealout_fills_defaults():
    deal = DealOut(id=1, title="X")
    assert deal.upvote_count == 0
    assert deal.downvote_count == 0
    assert deal.community_score == 0
    assert deal.user_vote is None
    assert deal.covered_regions == []


# --- SubmissionIn: not_blank validator ---

def test_submissionin_strips_whitespace():
    s = SubmissionIn(merchant_name="  KFC  ", description="  1-for-1 Zinger  ")
    assert s.merchant_name == "KFC"
    assert s.description == "1-for-1 Zinger"


@pytest.mark.parametrize("blank", ["", "   ", "\n\t"])
def test_submissionin_rejects_blank_merchant(blank):
    with pytest.raises(ValidationError):
        SubmissionIn(merchant_name=blank, description="a real deal")


@pytest.mark.parametrize("blank", ["", "   ", "\n\t"])
def test_submissionin_rejects_blank_description(blank):
    with pytest.raises(ValidationError):
        SubmissionIn(merchant_name="KFC", description=blank)


def test_submissionin_more_info_url_optional():
    s = SubmissionIn(merchant_name="KFC", description="deal")
    assert s.more_info_url is None
