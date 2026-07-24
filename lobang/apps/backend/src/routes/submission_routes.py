"""
Purpose: API endpoint for user-submitted deals.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from src.auth.supabase_auth import get_current_user
from src.schemas.deal_schema import DealOut
from src.schemas.submission_schema import SubmissionIn
from src.services.submission_service import (
    DuplicateSubmissionError,
    NotAFoodDealError,
    submit_deal,
)

submission_router = APIRouter()


@submission_router.post(
    "/submissions", response_model=DealOut, status_code=status.HTTP_201_CREATED
)
def create_submission(
    submission: SubmissionIn,
    user_id: str = Depends(get_current_user),
):
    try:
        return submit_deal(
            user_id,
            submission.merchant_name,
            submission.description,
            submission.more_info_url,
        )
    except NotAFoodDealError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "That doesn't look like a food deal. Mention the offer itself "
                "(e.g. the discount, 1-for-1, or price) in the description."
            ),
        )
    except DuplicateSubmissionError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This deal has already been submitted.",
        )
