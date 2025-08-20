# chapters
from typing import List, Optional
from mugennocore.interfaces.ichapter import IChapter
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.mapping.chapter_map import record_to_chapter


async def get_chapter_by_id(
    db: DatabaseProtocol, chapter_id: int
) -> Optional[IChapter]:
    row = await db.fetchrow("SELECT * FROM chapters WHERE id = $1", chapter_id)
    if row is None:
        return None
    return record_to_chapter(row)


async def get_all_chapters_by_manga_id(
    db: DatabaseProtocol, manga_id: int
) -> List[IChapter]:
    rows = await db.fetch(
        "SELECT * FROM chapters WHERE manga_id = $1 ORDER BY ch_number ASC", manga_id
    )
    return [chapter for row in rows if (chapter := record_to_chapter(row)) is not None]


async def insert_chapter(db: DatabaseProtocol, chapter: IChapter) -> int:
    query = """
        INSERT INTO chapters (manga_id, country_id, title, cover, ch_number)
        VALUES ($1, $2, $3, $4)
        RETURNING id
    """
    row = await db.fetchrow(
        query, chapter.manga_id, chapter.country_id, chapter.title, chapter.cover, chapter.ch_number
    )
    return row["id"] if row else -1
