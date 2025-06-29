from uuid import UUID
from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class IUser(Protocol):
    id: int
    user_name: str
    user_password: str
    user_role: str
    join_date: datetime
    email: str
    is_banned: bool
    nickname: str
    user_profile: UUID
    user_banner: UUID
    is_active: bool
    allow_nsfw: bool
    allow_dm: bool
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
