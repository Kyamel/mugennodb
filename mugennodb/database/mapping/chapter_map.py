from typing import Optional
from asyncpg import Record  # type: ignore
from mugennocore.model.chapter import Chapter


def record_to_chapter(row: Record) -> Optional[Chapter]:
    if row is None:
        return None
    return Chapter(
        id=row["id"],
        country_id=row["country_id"],
        manga_id=row["manga_id"],
        title=row["title"],
        ch_number=row["ch_number"],
        cover=row["cover"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )
