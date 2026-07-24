"""
Purpose: API endpoints for reading and updating the current user's preferences.
"""

from fastapi import APIRouter, Depends
from src.auth.supabase_auth import get_current_user
from src.schemas.preference_schema import PreferenceOut, PreferenceUpdate
from src.services.preference_service import (
  get_or_create_preferences,
  update_preferences,
)

preference_router = APIRouter()


@preference_router.get("/preferences", response_model=PreferenceOut)
def read_preferences(user_id: str = Depends(get_current_user)):
  return get_or_create_preferences(user_id)


@preference_router.put("/preferences", response_model=PreferenceOut)
def write_preferences(
  prefs: PreferenceUpdate,
  user_id: str = Depends(get_current_user),
):
  return update_preferences(user_id, prefs.model_dump())

