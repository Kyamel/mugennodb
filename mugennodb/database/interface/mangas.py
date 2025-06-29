# mangas
from typing import List, Optional
from mugennocore.interfaces.imanga import IManga
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.mapping.manga_map import record_to_manga


async def get_manga_by_id(db: DatabaseProtocol, manga_id: int) -> Optional[IManga]:
    row = await db.fetchrow("SELECT * FROM mangas WHERE id = $1", manga_id)
    if row is None:
        return None
    return record_to_manga(row)


async def search_mangas_by_title(db: DatabaseProtocol, title: str) -> List[IManga]:
    rows = await db.fetch(
        "SELECT * FROM mangas WHERE title_english ILIKE $1 OR title_native ILIKE $1",
        f"%{title}%",
    )
    return [manga for row in rows if (manga := record_to_manga(row)) is not None]


async def insert_manga(db: DatabaseProtocol, manga: IManga) -> int:
    query = """
        INSERT INTO mangas (
            title_english, title_native, release_date, finish_date,
            active_status, comic_type, cover, mal_id
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING id
    """
    row = await db.fetchrow(
        query,
        manga.title_english,
        manga.title_native,
        manga.release_date,
        manga.finish_date,
        manga.active_status,
        manga.comic_type,
        manga.cover,
        manga.mal_id,
    )
    return row["id"] if row else -1
