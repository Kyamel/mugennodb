from uuid import UUID
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.model.user_blocks import UserBlocksRead, UserBlocksCreate


# -------------------- READ --------------------

async def get_block(db: DatabaseProtocol, blocker_id: UUID, blocked_id: UUID) -> UserBlocksRead | None:
    query = """
        SELECT * FROM user_blocks
        WHERE blocker_id = $1 AND blocked_id = $2
    """
    row = await db.fetchrow(query, blocker_id, blocked_id)
    return UserBlocksRead(**dict(row)) if row else None


async def list_blocked(db: DatabaseProtocol, blocker_id: UUID) -> list[UserBlocksRead]:
    query = "SELECT * FROM user_blocks WHERE blocker_id = $1 ORDER BY created_at DESC"
    rows = await db.fetch(query, blocker_id)
    return [UserBlocksRead(**dict(r)) for r in rows]


async def list_blockers(db: DatabaseProtocol, blocked_id: UUID) -> list[UserBlocksRead]:
    query = "SELECT * FROM user_blocks WHERE blocked_id = $1 ORDER BY created_at DESC"
    rows = await db.fetch(query, blocked_id)
    return [UserBlocksRead(**dict(r)) for r in rows]


# -------------------- CREATE --------------------

async def create_block(db: DatabaseProtocol, data: UserBlocksCreate) -> UserBlocksRead:
    query = """
        INSERT INTO user_blocks (blocker_id, blocked_id)
        VALUES ($1, $2)
        RETURNING *
    """
    row = await db.fetchrow(query, data.blocker_id, data.blocked_id)
    return UserBlocksRead(**dict(row))


# -------------------- DELETE --------------------

async def delete_block(db: DatabaseProtocol, blocker_id: UUID, blocked_id: UUID) -> bool:
    query = "DELETE FROM user_blocks WHERE blocker_id = $1 AND blocked_id = $2"
    result = await db.execute(query, blocker_id, blocked_id)
    return result != "DELETE 0"
