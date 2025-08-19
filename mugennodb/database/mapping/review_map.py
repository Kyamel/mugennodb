from typing import Optional
from asyncpg import Record  # type: ignore
from mugennocore.model.reviews import Review


def record_to_review(record: Record) -> Optional[Review]:
    if record is None:
        return None
    return Review(
        review_id=record["review_id"],
        users_id=record["user_id"],
        score=record["score"],
        content=record["content"],
        created_at=record["created_at"],
        updated_at=record["updated_at"]
    )
