from typing import Optional
from asyncpg import Record
from mugennocore.model.related_manga import RelatedManga


def record_to_related_manga(row: Record) -> Optional[RelatedManga]:
    if row is None:
        return None
    return RelatedManga(
        id=row["id"],
        source_manga_id=row["source_manga_id"],
        related_manga_id=row["related_manga_id"],
        relationship_type=row["relationship_type"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )