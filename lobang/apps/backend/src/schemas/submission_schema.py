"""
Purpose: Describe the payload a user sends when submitting a deal
"""

from typing import Optional
from pydantic import BaseModel, field_validator


class SubmissionIn(BaseModel):
    merchant_name: str
    description: str
    more_info_url: Optional[str] = None

    @field_validator("merchant_name", "description")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value
