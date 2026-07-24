"""
Route tests for GET /api/v1/deals and /deals/for-you. The service layer is
patched so no database is touched; these assert routing, auth wiring, and that
responses validate against DealOut.
"""

from unittest.mock import patch


def test_list_deals_returns_validated_deals(client, as_guest):
    as_guest()
    fake = [
        {
            "id": 1,
            "title": "1-for-1 Coffee",
            "merchant_name": "Kopi Corner",
            "covered_regions": ["central"],
        }
    ]
    with patch("src.routes.deal_routes.get_deals", return_value=fake) as mock_get:
        resp = client.get("/api/v1/deals")

    assert resp.status_code == 200
    body = resp.json()
    assert body[0]["id"] == 1
    # DealOut defaults are filled in on the way out.
    assert body[0]["upvote_count"] == 0
    assert body[0]["covered_regions"] == ["central"]
    mock_get.assert_called_once_with(None)


def test_list_deals_passes_user_id_when_authenticated(client, as_user):
    user_id = as_user("user-abc")
    with patch("src.routes.deal_routes.get_deals", return_value=[]) as mock_get:
        resp = client.get("/api/v1/deals")

    assert resp.status_code == 200
    mock_get.assert_called_once_with(user_id)


def test_for_you_requires_authentication(client):
    # No auth override → the real bearer scheme rejects the missing token.
    resp = client.get("/api/v1/deals/for-you")
    assert resp.status_code in (401, 403)


def test_for_you_returns_deals_for_signed_in_user(client, as_user):
    user_id = as_user("user-xyz")
    fake = [{"id": 5, "title": "Ramen 50% off"}]
    with patch(
        "src.routes.deal_routes.get_for_you_deals", return_value=fake
    ) as mock_fy:
        resp = client.get("/api/v1/deals/for-you")

    assert resp.status_code == 200
    assert resp.json()[0]["id"] == 5
    mock_fy.assert_called_once_with(user_id)
