from typing import Optional
from asyncpg import Record  # type: ignore
from mugennocore.model.manga_review import MangaReview


def record_to_mangaReview(record: Record) -> Optional[MangaReview]:
    if record is None:
        return None
    return MangaReview(
        id=record["id"],
        review_id=record["review_id"],
        manga_id=record["manga_id"],
        created_at=record["created_at"],
        updated_at=record["updated_at"],
    )
