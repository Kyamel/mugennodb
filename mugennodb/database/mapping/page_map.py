from typing import Optional
from asyncpg import Record  # type: ignore
from mugennocore.model.page import Page


def record_to_page(row: Record) -> Optional[Page]:
    if row is None:
        return None
    return Page(
        id=row["id"],
        chapter_id=row["chapter_id"],
        pg_number=row["pg_number"],
        source=row["source"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )
