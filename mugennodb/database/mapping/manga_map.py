from asyncpg import Record  # type: ignore
from typing import Optional
from mugennocore.model.manga import Manga


def record_to_manga(row: Record) -> Optional[Manga]:
    if row is None:
        return None
    return Manga(
        id=row["id"],
        country_id=row["country_id"],
        title_english=row["title_english"],
        title_native=row["title_native"],
        release_date=row["release_date"],  # date
        finish_date=row["finish_date"],  # Optional[date]
        active_status=row["active_status"],
        comic_type=row["comic_type"],
        cover=row["cover"],  # UUID
        mal_id=row["mal_id"],
        created_at=row["created_at"],  # datetime
        updated_at=row["updated_at"],  # datetime
    )
