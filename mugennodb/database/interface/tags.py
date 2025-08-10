# tags

from typing import List, Optional
from mugennocore.interfaces.itag import ITag
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.mapping.tag_map import record_to_tag

async def get_tag_by_id(db: DatabaseProtocol, tag_id: int) -> Optional[ITag]:
    """Busca de uma tag pelo ID."""
    row = await db.fetchrow("SELECT * FROM tags WHERE id = $1", tag_id)
    if row is None:
        return None
    return record_to_tag(row)

async def get_all_tags(db: DatabaseProtocol) -> List[ITag]:
    """Busca todas as tags, ordenadas por nome."""
    rows = await db.fetch("SELECT * FROM tags ORDER BY tag_name ASC")
    return [tag for row in rows if (tag := record_to_tag(row)) is not None]

async def insert_tag(db: DatabaseProtocol, tag: ITag) -> None:
    """Insere uma nova tag no banco de dados."""
    query = """
        INSERT INTO tags (tag_name, tag_type)
        VALUES ($1, $2)
        RETURNING id
    """
    row = await db.fetchrow(query, tag.name, tag.type)
    return row["id"] if row else -1