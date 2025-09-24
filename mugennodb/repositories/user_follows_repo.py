from uuid import UUID
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennocore.model.user_follows import UserFollowsRead, UserFollowsCreate


# -------------------- READ --------------------

async def get_follow(db: DatabaseProtocol, follower_id: UUID, following_id: UUID) -> UserFollowsRead | None:
    query = """
        SELECT * FROM user_follows
        WHERE follower_id = $1 AND following_id = $2
    """
    row = await db.fetchrow(query, follower_id, following_id)
    return UserFollowsRead(**dict(row)) if row else None


async def list_followings(db: DatabaseProtocol, follower_id: UUID) -> list[UserFollowsRead]:
    query = "SELECT * FROM user_follows WHERE follower_id = $1 ORDER BY created_at DESC"
    rows = await db.fetch(query, follower_id)
    return [UserFollowsRead(**dict(r)) for r in rows]


async def list_followers(db: DatabaseProtocol, following_id: UUID) -> list[UserFollowsRead]:
    query = "SELECT * FROM user_follows WHERE following_id = $1 ORDER BY created_at DESC"
    rows = await db.fetch(query, following_id)
    return [UserFollowsRead(**dict(r)) for r in rows]


# -------------------- CREATE --------------------

async def create_follow(db: DatabaseProtocol, data: UserFollowsCreate) -> UserFollowsRead:
    query = """
        INSERT INTO user_follows (follower_id, following_id)
        VALUES ($1, $2)
        RETURNING *
    """
    row = await db.fetchrow(query, data.follower_id, data.following_id)
    return UserFollowsRead(**dict(row))


# -------------------- DELETE --------------------

async def delete_follow(db: DatabaseProtocol, follower_id: UUID, following_id: UUID) -> bool:
    query = "DELETE FROM user_follows WHERE follower_id = $1 AND following_id = $2"
    result = await db.execute(query, follower_id, following_id)
    return result != "DELETE 0"
