"""
Route tests for POST /api/v1/submissions. submit_deal is patched so the scraping
parse pipeline and DB never run; these assert auth, validation, the success
shape, and the error → HTTP status mapping.
"""

from unittest.mock import patch

from src.services.submission_service import (
    DuplicateSubmissionError,
    NotAFoodDealError,
)

VALID_PAYLOAD = {
    "merchant_name": "KFC",
    "description": "1-for-1 Zinger burger till 31 July, all outlets",
}


def test_submission_requires_authentication(client):
    resp = client.post("/api/v1/submissions", json=VALID_PAYLOAD)
    assert resp.status_code in (401, 403)


def test_submission_success_returns_created_deal(client, as_user):
    as_user("user-1")
    created = {"id": 10, "title": "KFC: 1-for-1 Zinger", "merchant_name": "KFC"}
    with patch(
        "src.routes.submission_routes.submit_deal", return_value=created
    ) as mock_submit:
        resp = client.post("/api/v1/submissions", json=VALID_PAYLOAD)

    assert resp.status_code == 201
    assert resp.json()["id"] == 10
    # user_id (from auth) is passed through as the first positional arg.
    assert mock_submit.call_args.args[0] == "user-1"


def test_submission_not_a_food_deal_returns_422(client, as_user):
    as_user()
    with patch(
        "src.routes.submission_routes.submit_deal", side_effect=NotAFoodDealError()
    ):
        resp = client.post("/api/v1/submissions", json=VALID_PAYLOAD)
    assert resp.status_code == 422


def test_submission_duplicate_returns_409(client, as_user):
    as_user()
    with patch(
        "src.routes.submission_routes.submit_deal",
        side_effect=DuplicateSubmissionError(),
    ):
        resp = client.post("/api/v1/submissions", json=VALID_PAYLOAD)
    assert resp.status_code == 409


def test_submission_blank_fields_rejected_before_service(client, as_user):
    as_user()
    with patch("src.routes.submission_routes.submit_deal") as mock_submit:
        resp = client.post(
            "/api/v1/submissions",
            json={"merchant_name": "   ", "description": "x"},
        )
    # SubmissionIn validation fails first → service never called.
    assert resp.status_code == 422
    mock_submit.assert_not_called()
