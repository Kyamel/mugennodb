from typing import Optional
from asyncpg import Record
from mugennocore.model.country import Country


def record_to_country(row: Record) -> Optional[Country]:
    if row is None:
        return None
    return Country(
        id=row["id"],
        lang=row["lang"],
        locale_code=row["locale_code"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )