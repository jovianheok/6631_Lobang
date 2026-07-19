"""
Purpose: API endpoints for viewing and casting votes on deals.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.supabase_auth import get_current_user, get_optional_current_user
from src.schemas.vote_schema import DealVoteSummary, VoteUpdate
from src.services.vote_service import get_vote_summary, remove_vote, set_vote

vote_router = APIRouter()


@vote_router.get("/deals/{deal_id}/votes", response_model=DealVoteSummary)
def get_votes(
    deal_id: int,
    user_id: str | None = Depends(get_optional_current_user),
):
    try:
        return get_vote_summary(deal_id, user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@vote_router.post("/deals/{deal_id}/vote", response_model=DealVoteSummary)
def create_or_update_vote(
    deal_id: int,
    payload: VoteUpdate,
    user_id: str = Depends(get_current_user),
):
    try:
        return set_vote(user_id, deal_id, payload.vote)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@vote_router.delete("/deals/{deal_id}/vote", response_model=DealVoteSummary)
def delete_vote(
    deal_id: int,
    user_id: str = Depends(get_current_user),
):
    try:
        return remove_vote(user_id, deal_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
