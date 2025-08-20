from typing import Optional
from asyncpg import Record
from mugennocore.model.manga_genre import MangaGenre


def record_to_manga_genre(row: Record) -> Optional[MangaGenre]:
    if row is None:
        return None
    return MangaGenre(
        id=row["id"],
        manga_id=row["manga_id"],
        tag_id=row["tag_id"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )
