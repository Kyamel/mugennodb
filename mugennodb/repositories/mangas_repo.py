from typing import Optional, List
from uuid import UUID
from dataclasses import fields
from datetime import date, datetime
from mugennocore.model.mangas import MangasCreate, MangasRead, MangasUpdate
from mugennocore.model.enums import EAgeRating, EMangaStatus
from mugennodb.conection.database_protocol import DatabaseProtocol


# -------------------- READ --------------------

async def get_manga_by_id(db: DatabaseProtocol, manga_id: UUID) -> Optional[MangasRead]:
    query = "SELECT * FROM mangas WHERE id = $1 AND deleted_at IS NULL"
    row = await db.fetchrow(query, manga_id)
    return MangasRead(**dict(row)) if row else None


async def list_mangas(db: DatabaseProtocol, limit: int = 100, offset: int = 0) -> List[MangasRead]:
    query = "SELECT * FROM mangas WHERE deleted_at IS NULL ORDER BY created_at DESC LIMIT $1 OFFSET $2"
    rows = await db.fetch(query, limit, offset)
    return [MangasRead(**dict(r)) for r in rows]


async def search_mangas_by_title(db: DatabaseProtocol, title: str, limit: int = 20, offset: int = 0) -> list[MangasRead]:
    query = """
        SELECT * FROM mangas
        WHERE title_english ILIKE $1 AND deleted_at IS NULL
        ORDER BY created_at DESC
        LIMIT $2 OFFSET $3
    """
    rows = await db.fetch(query, f"%{title}%", limit, offset)
    return [MangasRead(**dict(r)) for r in rows]

# -------------------- CREATE --------------------

async def create_manga(db: DatabaseProtocol, data: MangasCreate) -> MangasRead:
    # Campos e valores do dataclass
    data_fields = [f.name for f in fields(data)]
    values = [getattr(data, f) for f in data_fields]

    # Monta a query dinamicamente
    columns = ", ".join(data_fields)
    placeholders = ", ".join(f"${i+1}" for i in range(len(data_fields)))
    query = f"""
        INSERT INTO mangas ({columns})
        VALUES ({placeholders})
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return MangasRead(**dict(row))


# -------------------- UPDATE --------------------

async def update_manga(db: DatabaseProtocol, data: MangasUpdate) -> Optional[MangasRead]:
    # Pega apenas os campos que não são None e que não são "id"
    fields_to_update = {k: v for k, v in data.__dict__.items() if v is not None and k != "id"}
    if not fields_to_update:
        return await get_manga_by_id(db, data.id)

    set_clause = ", ".join(f"{k} = ${i+1}" for i, k in enumerate(fields_to_update.keys()))
    values = list(fields_to_update.values())
    values.append(data.id)

    query = f"""
        UPDATE mangas
        SET {set_clause}, updated_at = now()
        WHERE id = ${len(values)} AND deleted_at IS NULL
        RETURNING *
    """
    row = await db.fetchrow(query, *values)
    return MangasRead(**dict(row)) if row else None


# -------------------- SOFT DELETE --------------------

async def delete_manga(db: DatabaseProtocol, manga_id: UUID) -> bool:
    query = "UPDATE mangas SET deleted_at = now() WHERE id = $1 AND deleted_at IS NULL"
    result = await db.execute(query, manga_id)
    return result != "UPDATE 0"


# -------------------- RESTORE --------------------

async def restore_manga(db: DatabaseProtocol, manga_id: UUID) -> bool:
    query = "UPDATE mangas SET deleted_at = NULL WHERE id = $1 AND deleted_at IS NOT NULL"
    result = await db.execute(query, manga_id)
    return result != "UPDATE 0"
