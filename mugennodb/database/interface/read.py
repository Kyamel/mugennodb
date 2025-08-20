from mugennocore.interfaces.iread import IRead
from mugennodb.database.mapping.read_map import record_to_read
from mugennodb.conection.database_protocol import DatabaseProtocol
from typing import Optional


async def insert_read(db: DatabaseProtocol, read: IRead) -> bool:
    """
    Insere uma relação de leitura na tabela users_mangas.
    """
    record = await db.fetchrow(
        """
        INSERT INTO users_mangas (user_id, manga_id, status)
        VALUES ($1, $2, $3)
        RETURNING *
        """,
        read.user_id,
        read.manga_id,
        read.status,
    )
    return record_to_read(record) is not None


async def get_read(
    db: DatabaseProtocol, user_id: int, manga_id: int
) -> Optional[IRead]:
    """
    Busca uma leitura pelo par (user_id, manga_id).
    """
    record = await db.fetchrow(
        "SELECT * FROM users_mangas WHERE user_id=$1 AND manga_id=$2", user_id, manga_id
    )
    return record_to_read(record)


async def update_read_status(
    db: DatabaseProtocol, user_id: int, manga_id: int, status: str
) -> bool:
    """
    Atualiza o status de leitura.
    """
    record = await db.fetchrow(
        """
        UPDATE users_mangas
        SET status=$3, updated_at=NOW()
        WHERE user_id=$1 AND manga_id=$2
        RETURNING *
        """,
        user_id,
        manga_id,
        status,
    )
    return record_to_read(record) is not None


async def delete_read(db: DatabaseProtocol, user_id: int, manga_id: int) -> bool:
    """
    Remove uma leitura da tabela.
    """
    result = await db.execute(
        "DELETE FROM users_mangas WHERE user_id=$1 AND manga_id=$2", user_id, manga_id
    )
    return result == "DELETE 1"
