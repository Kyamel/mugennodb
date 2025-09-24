from typing import Optional
from uuid import UUID
from dataclasses import fields
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.model.manga_relationships import (
    MangaRelationshipsRead,
    MangaRelationshipsCreate,
    MangaRelationshipsUpdate
)

# -------------------- READ --------------------

async def get_relationship_by_id(db: DatabaseProtocol, rel_id: UUID) -> Optional[MangaRelationshipsRead]:
    query = "SELECT * FROM manga_relationships WHERE id = $1"
    row = await db.fetchrow(query, rel_id)
    return MangaRelationshipsRead(**dict(row)) if row else None


async def list_relationships_for_manga(db: DatabaseProtocol, manga_id: UUID) -> list[MangaRelationshipsRead]:
    query = """
        SELECT * FROM manga_relationships
        WHERE source_manga_id = $1 OR target_manga_id = $1
        ORDER BY created_at DESC
    """
    rows = await db.fetch(query, manga_id)
    return [MangaRelationshipsRead(**dict(r)) for r in rows]


# -------------------- CREATE --------------------

async def create_relationship(db: DatabaseProtocol, data: MangaRelationshipsCreate) -> MangaRelationshipsRead:
    data_fields = [f.name for f in fields(data)]
    values = [getattr(data, f) for f in data_fields]

    columns = ", ".join(data_fields)
    placeholders = ", ".join(f"${i+1}" for i in range(len(values)))

    query = f"""
        INSERT INTO manga_relationships ({columns})
        VALUES ({placeholders})
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return MangaRelationshipsRead(**dict(row))


# -------------------- UPDATE --------------------

async def update_relationship(db: DatabaseProtocol, data: MangaRelationshipsUpdate) -> Optional[MangaRelationshipsRead]:
    fields_to_update = {k: v for k, v in data.__dict__.items() if v is not None and k != "id"}
    if not fields_to_update:
        return await get_relationship_by_id(db, data.id)

    set_clause = ", ".join(f"{k} = ${i+1}" for i, k in enumerate(fields_to_update.keys()))
    values = list(fields_to_update.values())
    values.append(data.id)

    query = f"""
        UPDATE manga_relationships
        SET {set_clause}, updated_at = now()
        WHERE id = ${len(values)}
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return MangaRelationshipsRead(**dict(row)) if row else None


# -------------------- DELETE --------------------

async def delete_relationship(db: DatabaseProtocol, rel_id: UUID) -> bool:
    query = "DELETE FROM manga_relationships WHERE id = $1"
    result = await db.execute(query, rel_id)
    return result != "DELETE 0"
