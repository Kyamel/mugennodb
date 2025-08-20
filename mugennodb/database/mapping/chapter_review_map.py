from typing import Optional
from asyncpg import Record  # type: ignore
from mugennocore.model.chapter_review import ChapterReview


def record_to_chapter_review(record: Record) -> Optional[ChapterReview]:
    if record is None:
        return None
    return ChapterReview(review_id=record["review_id"], chapter_id=record["chapter_id"])
