from typing import Optional
from asyncpg import Record  # type: ignore
from mugennocore.model.user import User


def record_to_user(row: Record) -> Optional[User]:
    if row is None:
        return None
    return User(
        id=row["id"],
        user_name=row["user_name"],
        user_password=row["user_password"],
        user_role=row["user_role"],
        join_date=row["join_date"],
        email=row["email"],
        nickname=row["nickname"],
        user_profile=row["user_profile"],
        user_banner=row["user_banner"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        is_banned=row["is_banned"],
        is_active=row["is_active"],
        allow_nsfw=row["allow_nsfw"],
        allow_dm=row["allow_dm"],
    )
