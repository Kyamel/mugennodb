from typing import Optional
from uuid import UUID
from dataclasses import fields
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.model.chapters import ChaptersRead, ChaptersCreate, ChaptersUpdate

# -------------------- READ --------------------

async def get_chapter_by_id(db: DatabaseProtocol, chapter_id: UUID) -> Optional[ChaptersRead]:
    query = "SELECT * FROM chapters WHERE id = $1"
    row = await db.fetchrow(query, chapter_id)
    return ChaptersRead(**dict(row)) if row else None


async def list_chapters_for_manga(db: DatabaseProtocol, manga_id: UUID) -> list[ChaptersRead]:
    query = """
        SELECT *
        FROM chapters
        WHERE manga_id = $1
        ORDER BY
            CAST(REGEXP_REPLACE(ch_number, '[^0-9.]+', '', 'g') AS NUMERIC),
            REGEXP_REPLACE(ch_number, '^[0-9.]+', '', 'g')
    """
    rows = await db.fetch(query, manga_id)
    return [ChaptersRead(**dict(r)) for r in rows]

# -------------------- CREATE --------------------

async def create_chapter(db: DatabaseProtocol, data: ChaptersCreate) -> ChaptersRead:
    data_fields = [f.name for f in fields(data)]
    values = [getattr(data, f) for f in data_fields]

    columns = ", ".join(data_fields)
    placeholders = ", ".join(f"${i+1}" for i in range(len(values)))

    query = f"""
        INSERT INTO chapters ({columns})
        VALUES ({placeholders})
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return ChaptersRead(**dict(row))


# -------------------- UPDATE --------------------

async def update_chapter(db: DatabaseProtocol, data: ChaptersUpdate) -> Optional[ChaptersRead]:
    fields_to_update = {k: v for k, v in data.__dict__.items() if v is not None and k != "id"}
    if not fields_to_update:
        return await get_chapter_by_id(db, data.id)

    set_clause = ", ".join(f"{k} = ${i+1}" for i, k in enumerate(fields_to_update.keys()))
    values = list(fields_to_update.values())
    values.append(data.id)

    query = f"""
        UPDATE chapters
        SET {set_clause}, updated_at = now()
        WHERE id = ${len(values)}
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return ChaptersRead(**dict(row)) if row else None


# -------------------- DELETE --------------------

async def delete_chapter(db: DatabaseProtocol, chapter_id: UUID) -> bool:
    query = "DELETE FROM chapters WHERE id = $1"
    result = await db.execute(query, chapter_id)
    return result != "DELETE 0"
