"""
Purpose: API endpoints for saving, removing, and listing the current user's bookmarked deals.
"""

from fastapi import APIRouter, Depends, status
from src.auth.supabase_auth import get_current_user
from src.schemas.deal_schema import DealOut
from src.schemas.bookmark_schema import BookmarkCreate
from src.services.bookmark_service import (
    add_bookmark,
    remove_bookmark,
    get_bookmarked_deals,
)

bookmark_router = APIRouter()


@bookmark_router.get("/bookmarks", response_model=list[DealOut])
def list_bookmarks(user_id: str = Depends(get_current_user)):
    return get_bookmarked_deals(user_id)


@bookmark_router.post("/bookmarks", status_code=status.HTTP_204_NO_CONTENT)
def create_bookmark(
    bookmark: BookmarkCreate,
    user_id: str = Depends(get_current_user),
):
    add_bookmark(user_id, bookmark.deal_id)


@bookmark_router.delete("/bookmarks/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(
    deal_id: int,
    user_id: str = Depends(get_current_user),
):
    remove_bookmark(user_id, deal_id)
