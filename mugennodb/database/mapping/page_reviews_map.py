from typing import Optional
from asyncpg import Record  # type: ignore
from mugennocore.model.page_review import PageReview


def record_to_pageReview(record: Record) -> Optional[PageReview]:
    if record is None:
        return None
    return PageReview(
        id=record["id"],
        review_id=record["review_id"],
        page_id=record["page_id"],
        created_at=record["created_at"],
        updated_at=record["updated_at"],
    )
