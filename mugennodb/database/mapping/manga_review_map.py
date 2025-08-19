from typing import Optional
from asyncpg import Record  # type: ignore
from mugennocore.model.manga_review import User

def record_to_mangaReview(record: Record) -> Optional[User]:
    if row is None:
        return None
    return User(
            id=record['id'],
            reviewId=record['reviewId'],
            mangaId=record['mangaId'],
    )