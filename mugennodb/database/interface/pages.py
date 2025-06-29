# pages
from typing import Optional

from asyncpg import Record  # type: ignore
from mugennocore.interfaces.ipage import IPage
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.mapping.page_map import record_to_page


async def get_page_by_id(db: DatabaseProtocol, page_id: int) -> Optional[IPage]:
    row: Optional[Record] = await db.fetchrow(
        "SELECT * FROM pages WHERE id = $1", page_id
    )
    if row is None:
        return None
    return record_to_page(row)


async def get_page_by_chapter_and_number(
    db: DatabaseProtocol, chapter_id: int, pg_number: int
) -> Optional[IPage]:
    row = await db.fetchrow(
        "SELECT * FROM pages WHERE chapter_id = $1 AND pg_number = $2",
        chapter_id,
        pg_number,
    )
    if row is None:
        return None
    return record_to_page(row)


async def insert_page(db: DatabaseProtocol, page: IPage) -> int:
    query = """
        INSERT INTO pages (chapter_id, pg_number, source)
        VALUES ($1, $2, $3)
        RETURNING id
    """
    row = await db.fetchrow(query, page.chapter_id, page.pg_number, page.source)
    return row["id"] if row else -1
