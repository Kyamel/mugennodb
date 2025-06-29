# users
from typing import List, Optional

from asyncpg import Record  # type: ignore
from mugennocore.interfaces.iuser import IUser
from mugennodb.conection.database_protocol import DatabaseProtocol
from mugennodb.database.mapping.user_map import record_to_user


async def get_user_by_id(db: DatabaseProtocol, user_id: int) -> Optional[IUser]:
    row: Optional[Record] = await db.fetchrow(
        "SELECT * FROM users WHERE id = $1", user_id
    )
    if row is None:
        return None
    return record_to_user(row)


async def search_users_by_name(db: DatabaseProtocol, username: str) -> List[IUser]:
    rows = await db.fetch(
        "SELECT * FROM users WHERE user_name ILIKE $1 OR nickname ILIKE $1",
        f"%{username}%",
    )
    return [user for row in rows if (user := record_to_user(row)) is not None]


async def insert_user(db: DatabaseProtocol, user: IUser) -> int:
    query = """
        INSERT INTO users (
            user_name, user_password, user_role, join_date, email,
            is_banned, nickname, user_profile, user_banner,
            is_active, allow_nsfw, allow_dm
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        RETURNING id
    """
    row = await db.fetchrow(
        query,
        user.user_name,
        user.user_password,
        user.user_role,
        user.join_date,
        user.email,
        user.is_banned,
        user.nickname,
        user.user_profile,
        user.user_banner,
        user.is_active,
        user.allow_nsfw,
        user.allow_dm,
    )
    return row["id"] if row else -1
