"""
Purpose: Shape of vote payloads and aggregated vote summaries.
"""

from typing import Literal, Optional

from pydantic import BaseModel


class VoteUpdate(BaseModel):
    vote: Literal[1, -1]


class DealVoteSummary(BaseModel):
    deal_id: int
    upvote_count: int
    downvote_count: int
    community_score: int
    user_vote: Optional[int] = None
