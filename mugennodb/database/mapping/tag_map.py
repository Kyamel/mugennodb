from typing import Optional
from asyncpg import Record
from mugennocore.model.tag import Tag


def record_to_tag(row: Record) -> Optional[Tag]:
    if row is None:
        return None
    return Tag(
        id=row["id"],
        name=row["tag_name"],
        type=row["tag_type"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )
