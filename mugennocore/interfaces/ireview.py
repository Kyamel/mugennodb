from typing import Protocol, runtime_checkable
from datetime import datetime


@runtime_checkable
class IReview(Protocol):
    review_id: int
    user_id: int
    score: float
    content: str
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
