from typing import Protocol, runtime_checkable
from datetime import datetime


@runtime_checkable
class IMangaReview(Protocol):
    id: int
    review_id: int
    manga_id: int
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
