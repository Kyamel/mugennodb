from typing import List, Optional, Tuple
from mugennocore.interfaces.imanga import IManga
from mugennocore.interfaces.irelated_manga import IRelatedManga
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.mapping.manga_map import record_to_manga


async def add_relationship(db: DatabaseProtocol, relationship: IRelatedManga) -> int:
    """Adiciona uma nova relação entre dois mangás no banco de dados."""
    query = """
        INSERT INTO related_mangas (source_manga_id, related_manga_id, relationship_type)
        VALUES ($1, $2, $3)
        RETURNING id
    """
    row = await db.fetchrow(
        query,
        relationship.source_manga_id,
        relationship.related_manga_id,
        relationship.relationship_type,
    )
    return row["id"] if row else -1


async def get_related_mangas_by_source_id(
    db: DatabaseProtocol, source_manga_id: int
) -> List[Tuple[IManga, str]]:
    """Busca todos os mangás relacionados a um mangá de origem.
    Retorna uma lista de tuplas, onde cada tupla contém:
    (objeto Manga do mangá relacionado, tipo da relação como string)"""
    query = """
        SELECT m.*, rm.relationship_type
        FROM mangas m
        JOIN related_mangas rm ON m.id = rm.related_manga_id
        WHERE rm.source_manga_id = $1
    """
    rows = await db.fetch(query, source_manga_id)

    results: List[Tuple[IManga, str]] = []
    for row in rows:
        manga = record_to_manga(row)
        if manga:
            relationship_type = row["relationship_type"]
            results.append((manga, relationship_type))

    return results


async def remove_relationship(db: DatabaseProtocol, relationship_id: int) -> None:
    """Remove uma relação específica pelo ID único."""
    await db.execute("DELETE FROM related_mangas WHERE id = $1", relationship_id)
