from typing import Optional
from uuid import UUID
from dataclasses import fields
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.model.manga_external_sources import (
    MangaExternalSourcesRead,
    MangaExternalSourcesCreate,
    MangaExternalSourcesUpdate,
)


# -------------------- READ --------------------

async def get_source_by_id(db: DatabaseProtocol, source_id: UUID) -> Optional[MangaExternalSourcesRead]:
    query = "SELECT * FROM manga_external_sources WHERE id = $1"
    row = await db.fetchrow(query, source_id)
    return MangaExternalSourcesRead(**dict(row)) if row else None


async def list_sources_by_manga(db: DatabaseProtocol, manga_id: UUID, limit: int = 100, offset: int = 0) -> list[MangaExternalSourcesRead]:
    query = """
        SELECT * FROM manga_external_sources
        WHERE manga_id = $1
        ORDER BY created_at DESC
        LIMIT $2 OFFSET $3
    """
    rows = await db.fetch(query, manga_id, limit, offset)
    return [MangaExternalSourcesRead(**dict(r)) for r in rows]


# -------------------- CREATE --------------------

async def create_source(db: DatabaseProtocol, data: MangaExternalSourcesCreate) -> MangaExternalSourcesRead:
    data_fields = [f.name for f in fields(data)]
    values = [getattr(data, f) for f in data_fields]

    columns = ", ".join(data_fields)
    placeholders = ", ".join(f"${i+1}" for i in range(len(values)))

    query = f"""
        INSERT INTO manga_external_sources ({columns})
        VALUES ({placeholders})
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return MangaExternalSourcesRead(**dict(row))


# -------------------- UPDATE --------------------

async def update_source(db: DatabaseProtocol, data: MangaExternalSourcesUpdate) -> Optional[MangaExternalSourcesRead]:
    fields_to_update = {k: v for k, v in data.__dict__.items() if v is not None and k != "id"}
    if not fields_to_update:
        return await get_source_by_id(db, data.id)

    set_clause = ", ".join(f"{k} = ${i+1}" for i, k in enumerate(fields_to_update.keys()))
    values = list(fields_to_update.values())
    values.append(data.id)

    query = f"""
        UPDATE manga_external_sources
        SET {set_clause}, updated_at = now()
        WHERE id = ${len(values)}
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return MangaExternalSourcesRead(**dict(row)) if row else None


# -------------------- DELETE --------------------

async def delete_source(db: DatabaseProtocol, source_id: UUID) -> bool:
    query = "DELETE FROM manga_external_sources WHERE id = $1"
    result = await db.execute(query, source_id)
    return result != "DELETE 0"
