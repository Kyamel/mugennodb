from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class PageReview:
    id: int
    review_id: int
    page_id: int
    created_at: datetime
    updated_at: datetime
