from typing import Optional
from uuid import UUID
from dataclasses import fields
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.model.manga_external_links import (
    MangaExternalLinksRead,
    MangaExternalLinksCreate,
    MangaExternalLinksUpdate
)


# -------------------- READ --------------------

async def get_external_link_by_id(db: DatabaseProtocol, link_id: UUID) -> Optional[MangaExternalLinksRead]:
    query = "SELECT * FROM manga_external_links WHERE id = $1"
    row = await db.fetchrow(query, link_id)
    return MangaExternalLinksRead(**dict(row)) if row else None


async def list_external_links_for_manga(db: DatabaseProtocol, manga_id: UUID) -> list[MangaExternalLinksRead]:
    query = """
        SELECT * FROM manga_external_links
        WHERE manga_id = $1
        ORDER BY created_at DESC
    """
    rows = await db.fetch(query, manga_id)
    return [MangaExternalLinksRead(**dict(r)) for r in rows]


# -------------------- CREATE --------------------

async def create_external_link(db: DatabaseProtocol, data: MangaExternalLinksCreate) -> MangaExternalLinksRead:
    data_fields = [f.name for f in fields(data)]
    values = [getattr(data, f) for f in data_fields]

    columns = ", ".join(data_fields)
    placeholders = ", ".join(f"${i+1}" for i in range(len(values)))

    query = f"""
        INSERT INTO manga_external_links ({columns})
        VALUES ({placeholders})
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return MangaExternalLinksRead(**dict(row))


# -------------------- UPDATE --------------------

async def update_external_link(db: DatabaseProtocol, data: MangaExternalLinksUpdate) -> Optional[MangaExternalLinksRead]:
    fields_to_update = {k: v for k, v in data.__dict__.items() if v is not None and k != "id"}
    if not fields_to_update:
        return await get_external_link_by_id(db, data.id)

    set_clause = ", ".join(f"{k} = ${i+1}" for i, k in enumerate(fields_to_update.keys()))
    values = list(fields_to_update.values())
    values.append(data.id)

    query = f"""
        UPDATE manga_external_links
        SET {set_clause}, updated_at = now()
        WHERE id = ${len(values)}
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return MangaExternalLinksRead(**dict(row)) if row else None


# -------------------- DELETE --------------------

async def delete_external_link(db: DatabaseProtocol, link_id: UUID) -> bool:
    query = "DELETE FROM manga_external_links WHERE id = $1"
    result = await db.execute(query, link_id)
    return result != "DELETE 0"
