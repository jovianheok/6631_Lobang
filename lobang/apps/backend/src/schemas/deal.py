# Defines what a deal should look like

from pydantic import BaseModel                  # Imports the base class used for structured data models.
from typing import List                         # Imports List so we can say “this field is a list of strings.”


class DealOut(BaseModel):
    id: int
    title: str
    merchant_name: str
    distance_km: float
    score: float
    status: str
    verification_status: str
    end_time: str | None = None
    reason: List[str]