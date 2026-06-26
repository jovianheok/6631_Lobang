"""
Purpose: Read and write a user's preference row in public.user_profiles.
"""

from typing import Any
from src.database.connection import get_conn

# Columns returned to the client, in a fixed order shared by both queries
_COLUMNS = """
  user_id, display_name, max_price_level, cuisine_preferences,
  preferred_regions, home_latitude, home_longitude, max_distance_km
"""


def _row_to_dict(row: tuple) -> dict[str, Any]:
  return {
      "user_id": str(row[0]),
      "display_name": row[1],
      "max_price_level": row[2],
      "cuisine_preferences": row[3] or [],
      "preferred_regions": row[4] or [],
      "home_latitude": row[5],
      "home_longitude": row[6],
      "max_distance_km": float(row[7]) if row[7] is not None else None,
  }


def get_or_create_preferences(user_id: str) -> dict[str, Any]:
  """Return the user's preferences, creating an empty row on first access."""
  conn = get_conn()
  try:
      with conn.cursor() as cur:
          cur.execute(
              f"SELECT {_COLUMNS} FROM public.user_profiles WHERE user_id = %s;",
              (user_id,),
          )
          row = cur.fetchone()

          if row is None:
              cur.execute(
                  f"""
                  INSERT INTO public.user_profiles (user_id)
                  VALUES (%s)
                  RETURNING {_COLUMNS};
                  """,
                  (user_id,),
              )
              row = cur.fetchone()
              conn.commit()

          return _row_to_dict(row)
  finally:
      conn.close()


def update_preferences(user_id: str, data: dict[str, Any]) -> dict[str, Any]:
  """Upsert the full preference set for a user and return the saved row."""
  conn = get_conn()
  try:
      with conn.cursor() as cur:
          cur.execute(
              f"""
              INSERT INTO public.user_profiles
                  (user_id, display_name, max_price_level, cuisine_preferences,
                   preferred_regions, home_latitude, home_longitude, max_distance_km)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
              ON CONFLICT (user_id) DO UPDATE SET
                  display_name        = EXCLUDED.display_name,
                  max_price_level     = EXCLUDED.max_price_level,
                  cuisine_preferences = EXCLUDED.cuisine_preferences,
                  preferred_regions   = EXCLUDED.preferred_regions,
                  home_latitude       = EXCLUDED.home_latitude,
                  home_longitude      = EXCLUDED.home_longitude,
                  max_distance_km     = EXCLUDED.max_distance_km,
                  updated_at          = NOW()
              RETURNING {_COLUMNS};
              """,
              (
                  user_id,
                  data.get("display_name"),
                  data.get("max_price_level"),
                  data.get("cuisine_preferences") or [],
                  data.get("preferred_regions") or [],
                  data.get("home_latitude"),
                  data.get("home_longitude"),
                  data.get("max_distance_km"),
              ),
          )
          row = cur.fetchone()
          conn.commit()
          return _row_to_dict(row)
  finally:
      conn.close()

