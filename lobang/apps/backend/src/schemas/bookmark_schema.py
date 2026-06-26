"""
Purpose: Shape of the bookmark payloads exchanged with the client.
"""

from pydantic import BaseModel


class BookmarkCreate(BaseModel):
    deal_id: int
