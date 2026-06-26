"""
Purpose: Shape of the user-preferences payloads exchanged with the client.
"""

from pydantic import BaseModel
from typing import Optional


class PreferenceUpdate(BaseModel):
  display_name: Optional[str] = None
  max_price_level: Optional[int] = None      # 0..4, None = any price
  cuisine_preferences: list[str] = []        # canonical cuisine labels
  preferred_regions: list[str] = []          # SG regions
  home_latitude: Optional[float] = None      # distance model
  home_longitude: Optional[float] = None
  max_distance_km: Optional[float] = None


class PreferenceOut(PreferenceUpdate):
  user_id: str
