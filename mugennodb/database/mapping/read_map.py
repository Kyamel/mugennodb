from typing import Optional
from asyncpg import Record  # type: ignore
from mugennocore.model.read import Read

def record_to_read(record: Record) -> Optional[Read]:
    if record is None:
        return None
    return Read(
        user_id=record["user_id"],
        manga_id=record["manga_id"],
        status=record["status"],
        created_at=record["created_at"],
        updated_at=record["updated_at"]
    )
