from typing import List
from mugennocore.interfaces.itag import ITag
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.mapping.tag_map import record_to_tag


async def add_genre_to_manga(db: DatabaseProtocol, manga_id: int, tag_id: int) -> int:
    """Associa uma tag de gênero a um mangá.Retorna o ID da nova linha na tabela de junção."""
    query = """
        INSERT INTO manga_genres (manga_id, tag_id)
        VALUES ($1, $2)
        ON CONFLICT (manga_id, tag_id) DO NOTHING
        RETURNING id
    """
    row = await db.fetchrow(query, manga_id, tag_id)
    return row["id"] if row else -1


async def get_genres_for_manga(db: DatabaseProtocol, manga_id: int) -> List[ITag]:
    """Busca todas as tags do tipo 'GENRE' associadas a um mangá específico."""
    query = """
        SELECT t.*
        FROM tags t
        JOIN manga_genres mg ON t.id = mg.tag_id
        WHERE mg.manga_id = $1 AND t.tag_type = 'GENRE'
        ORDER BY t.tag_name ASC
    """
    rows = await db.fetch(query, manga_id)
    return [tag for row in rows if (tag := record_to_tag(row)) is not None]


async def remove_genre_from_manga(db: DatabaseProtocol, manga_id: int, tag_id: int) -> None:
    """Remove a associação de um gênero de um mangá."""
    await db.execute(
        "DELETE FROM manga_genres WHERE manga_id = $1 AND tag_id = $2",
        manga_id,
        tag_id,
    )