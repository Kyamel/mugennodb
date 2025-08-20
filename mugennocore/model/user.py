from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class User:
    id: int
    country_id: int
    user_name: str
    user_password: str
    user_role: str
    join_date: datetime
    email: str
    nickname: str
    user_profile: UUID
    user_banner: UUID
    created_at: datetime
    updated_at: datetime

    is_banned: bool = False
    is_active: bool = True
    allow_nsfw: bool = False
    allow_dm: bool = False

    def __str__(self) -> str:
        return f"User {self.user_name} ({self.email})"

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, user_name={self.user_name!r}, email={self.email!r}, "
            f"is_active={self.is_active}, is_banned={self.is_banned})"
        )
